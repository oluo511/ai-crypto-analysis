from langchain.tools import Tool
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import BedrockChat
from tools.web_search import WebSearch
import boto3
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class CryptoAnalysisAgent:
    def __init__(self):
        """Initialize LangChain-based crypto analysis agent"""
        
        self.aws_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-west-2")
        )
        
        model_kwargs = { 
            "max_tokens": 4096,
            "temperature": 0.3,
            "top_k": 250,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman"],
        }
        
        self.llm = BedrockChat(
            client=self.aws_client,
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            model_kwargs=model_kwargs,
        )
        
        self.search_client = WebSearch()
        self.tools = self._create_tools()
        
        # Create agent
        prompt = hub.pull("hwchase17/structured-chat-agent")
        agent = create_structured_chat_agent(self.llm, self.tools, prompt)
        
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            verbose=True, 
            handle_parsing_errors=True,
            max_iterations=10,
            return_intermediate_steps=True
        )
        
        logging.info("✅ LangChain Crypto Agent initialized successfully")
    
    def _create_tools(self):
        def search_whitepaper(query: str) -> str:
            try:
                results = self.search_client.search_whitepaper(query, num_results=3)
                if isinstance(results, dict) and 'error' in results:
                    return f"Error searching whitepaper: {results['error']}"
                
                if not results or len(results) == 0:
                    return f"No whitepaper results found for {query}"
                
                return "\n\n".join(
                    f"{i+1}. {item.get('title', 'No title')}\nSummary: {item.get('snippet', 'No summary')}\nLink: {item.get('link', 'No link')}"
                    for i, item in enumerate(results)
                )
            except Exception as e:
                logging.error(f"Error in search_whitepaper: {str(e)}")
                return f"Error searching whitepaper: {str(e)}"

        def search_crypto_news(query: str) -> str:
            try:
                results = self.search_client.search_latest_news(query, num_results=6)
                if isinstance(results, dict) and 'error' in results:
                    return f"Error searching news: {results['error']}"
                
                if not results or len(results) == 0:
                    return f"No news results found for {query}"
                
                return "\n\n".join(
                    f"Article {i+1}:\nTitle: {item.get('title', 'No title')}\nSummary: {item.get('snippet', 'No summary')}\nLink: {item.get('link', 'No link')}"
                    for i, item in enumerate(results)
                )
            except Exception as e:
                logging.error(f"Error in search_crypto_news: {str(e)}")
                return f"Error searching news: {str(e)}"

        def search_price_data(query: str) -> str:
            try:
                import requests
                search_url = "https://api.coingecko.com/api/v3/search"
                r = requests.get(search_url, params={'query': query}, timeout=10)
                
                if r.status_code != 200:
                    return f"Failed to search for {query} on CoinGecko (status: {r.status_code})"
                
                coins = r.json().get("coins", [])
                if not coins:
                    return f"No CoinGecko data found for {query}"

                coin_id = coins[0]["id"]
                r = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}", timeout=10)
                if r.status_code != 200:
                    return f"Failed to fetch market data for {query} (status: {r.status_code})"

                coin_data = r.json()
                d = coin_data.get("market_data", {})
                
                if not d:
                    return f"No market data available for {query}"
                
                return (
                    f"Current price data for {query}:\n"
                    f"Name: {coin_data.get('name', 'Unknown')}\n"
                    f"Symbol: {coin_data.get('symbol', 'Unknown').upper()}\n"
                    f"Price: ${d.get('current_price', {}).get('usd', 'N/A')}\n"
                    f"Market Cap: ${d.get('market_cap', {}).get('usd', 'N/A')}\n"
                    f"24h Change: {d.get('price_change_percentage_24h', 'N/A')}%\n"
                    f"7d Change: {d.get('price_change_percentage_7d', 'N/A')}%\n"
                    f"Volume: ${d.get('total_volume', {}).get('usd', 'N/A')}\n"
                    f"Rank: #{d.get('market_cap_rank', 'N/A')}"
                )
            except Exception as e:
                logging.error(f"Error in search_price_data: {str(e)}")
                return f"Error fetching price data: {str(e)}"

        tools = [
            Tool(
                name="search_whitepaper",
                func=search_whitepaper,
                description="Search for cryptocurrency whitepapers, technical documentation, and project details."
            ),
            Tool(
                name="search_reddit_sentiment",
                func=self.search_reddit_sentiment_tool,
                description="Search Reddit for community sentiment and opinions about cryptocurrencies."
            ),
            Tool(
                name="search_crypto_news",
                func=search_crypto_news,
                description="Search for latest cryptocurrency news and announcements."
            ),
            Tool(
                name="get_price_data",
                func=search_price_data,
                description="Get current price, market cap, and volume data for cryptocurrencies."
            )
        ]
        
        return tools
    
    def search_reddit_sentiment_tool(self, query: str) -> str:
        """Wrapper for LangChain tool usage (string return only)."""
        try:
            result = self.analyze_sentiment(query)
            if isinstance(result, dict) and 'analysis' in result:
                return result['analysis']
            else:
                return f"Sentiment analysis completed for {query}, but no detailed analysis available."
        except Exception as e:
            logging.error(f"Error in search_reddit_sentiment_tool: {str(e)}")
            return f"Error analyzing sentiment: {str(e)}"

    def analyze_sentiment(self, crypto_input):
        """Enhanced sentiment analysis with better error handling and fallback logic"""
        try:
            logging.info(f"Starting sentiment analysis for: {crypto_input}")
            
            # Try to get Reddit sentiment data
            results = self.search_client.search_reddit_sentiment(crypto_input, num_results=8)
            
            # Check for errors in results
            if isinstance(results, dict) and 'error' in results:
                logging.warning(f"Reddit search error: {results['error']}")
                return {
                    "analysis": f"Reddit sentiment search encountered an error: {results['error']}",
                    "positive": [],
                    "negative": [],
                    "neutral": []
                }
            
            # Check if results is None or empty
            if not results:
                logging.warning("No Reddit results returned")
                return {
                    "analysis": f"No Reddit sentiment data found for {crypto_input}. This could be due to API limitations or the search term not being popular on Reddit.",
                    "positive": [],
                    "negative": [],
                    "neutral": []
                }
            
            # Handle different result formats
            if isinstance(results, dict):
                positive_posts = results.get('positive', [])
                negative_posts = results.get('negative', [])
                neutral_posts = results.get('neutral', [])
            elif isinstance(results, list):
                # If results is a simple list, try to categorize based on keywords
                positive_posts = []
                negative_posts = []
                neutral_posts = []
                
                positive_keywords = ['buy', 'bullish', 'moon', 'pump', 'good', 'great', 'excellent', 'rising', 'up']
                negative_keywords = ['sell', 'bearish', 'dump', 'crash', 'bad', 'terrible', 'falling', 'down', 'scam']
                
                for post in results:
                    if not isinstance(post, dict):
                        continue
                        
                    title = post.get('title', '').lower()
                    snippet = post.get('snippet', '').lower()
                    text = f"{title} {snippet}"
                    
                    if any(keyword in text for keyword in positive_keywords):
                        positive_posts.append(post)
                    elif any(keyword in text for keyword in negative_keywords):
                        negative_posts.append(post)
                    else:
                        neutral_posts.append(post)
            else:
                logging.warning(f"Unexpected results format: {type(results)}")
                return {
                    "analysis": f"Unexpected data format received from Reddit search for {crypto_input}",
                    "positive": [],
                    "negative": [],
                    "neutral": []
                }

            # Create summary
            total_posts = len(positive_posts) + len(negative_posts) + len(neutral_posts)
            
            if total_posts == 0:
                summary = f"No Reddit posts found for {crypto_input}. This might indicate low discussion volume or the search term needs adjustment."
            else:
                summary = f"Reddit sentiment analysis for {crypto_input} (Total posts analyzed: {total_posts}):\n\n"
                
                # Add positive posts
                if positive_posts:
                    summary += f"🟢 POSITIVE SENTIMENT ({len(positive_posts)} posts):\n"
                    for i, post in enumerate(positive_posts[:3], 1):
                        title = post.get('title', 'No title')
                        summary += f"• Post {i}: {title}\n"
                    summary += "\n"
                
                # Add negative posts
                if negative_posts:
                    summary += f"🔴 NEGATIVE SENTIMENT ({len(negative_posts)} posts):\n"
                    for i, post in enumerate(negative_posts[:3], 1):
                        title = post.get('title', 'No title')
                        summary += f"• Post {i}: {title}\n"
                    summary += "\n"
                
                # Add neutral posts
                if neutral_posts:
                    summary += f"🟡 NEUTRAL SENTIMENT ({len(neutral_posts)} posts):\n"
                    for i, post in enumerate(neutral_posts[:3], 1):
                        title = post.get('title', 'No title')
                        summary += f"• Post {i}: {title}\n"
                    summary += "\n"
                
                # Add sentiment overview
                if total_posts > 0:
                    pos_pct = (len(positive_posts) / total_posts) * 100
                    neg_pct = (len(negative_posts) / total_posts) * 100
                    neu_pct = (len(neutral_posts) / total_posts) * 100
                    
                    summary += f"SENTIMENT BREAKDOWN:\n"
                    summary += f"• Positive: {pos_pct:.1f}%\n"
                    summary += f"• Negative: {neg_pct:.1f}%\n"
                    summary += f"• Neutral: {neu_pct:.1f}%\n"

            return {
                "analysis": summary,
                "positive": positive_posts,
                "negative": negative_posts,
                "neutral": neutral_posts
            }

        except Exception as e:
            logging.error(f"Error in analyze_sentiment: {str(e)}")
            return {
                "analysis": f"Error analyzing sentiment for {crypto_input}: {str(e)}",
                "positive": [],
                "negative": [],
                "neutral": []
            }

    def analyze_news_headlines(self, crypto_input):
        """Enhanced news analysis with better error handling"""
        prompt = f"""Search for latest news about {crypto_input} and categorize the findings.
        
        Please analyze and categorize as:

        **BULLISH NEWS:**
        - Positive developments and partnerships

        **BEARISH NEWS:**
        - Negative developments or concerns

        **NEUTRAL NEWS:**
        - Informational updates without clear market impact

        **MARKET IMPACT:**
        - How this news might affect price and investor sentiment"""

        try:
            llm_result = self.agent_executor.invoke({"input": prompt})
            summary = llm_result.get("output", "No analysis available")

            # Get news data
            news_data = self.search_client.search_latest_news(crypto_input, num_results=6)
            
            if isinstance(news_data, dict) and "error" in news_data:
                logging.warning(f"News search error: {news_data['error']}")
                return {
                    "analysis": f"{summary}\n\nNote: News search encountered an error: {news_data['error']}",
                    "bullish": [],
                    "neutral": [],
                    "bearish": []
                }
            
            if not news_data:
                return {
                    "analysis": f"{summary}\n\nNote: No recent news articles found for {crypto_input}",
                    "bullish": [],
                    "neutral": [],
                    "bearish": []
                }

            # Categorize news
            bullish, neutral, bearish = [], [], []
            
            bullish_keywords = ["partnership", "rally", "gain", "surge", "bull", "breakout", "adoption", "integration", "upgrade", "positive"]
            bearish_keywords = ["lawsuit", "drop", "fall", "loss", "bear", "crash", "hack", "ban", "regulation", "negative"]
            
            for item in news_data:
                if not isinstance(item, dict):
                    continue
                    
                title = item.get("title", "").lower()
                snippet = item.get("snippet", "").lower()
                text = f"{title} {snippet}"

                if any(word in text for word in bullish_keywords):
                    bullish.append(item)
                elif any(word in text for word in bearish_keywords):
                    bearish.append(item)
                else:
                    neutral.append(item)

            return {
                "analysis": summary,
                "bullish": bullish,
                "neutral": neutral,
                "bearish": bearish
            }

        except Exception as e:
            logging.error(f"Error in analyze_news_headlines: {str(e)}")
            return {
                "analysis": f"Error analyzing news for {crypto_input}: {str(e)}",
                "bullish": [],
                "neutral": [],
                "bearish": []
            }

    def summarize_whitepaper(self, crypto_input):
        """Enhanced whitepaper analysis with better error handling"""
        prompt = f"Search for and provide a comprehensive summary of the {crypto_input} whitepaper, focusing on key technical features, use cases, and project goals."
        try:
            result = self.agent_executor.invoke({"input": prompt})
            return result.get("output", f"No whitepaper analysis available for {crypto_input}")
        except Exception as e:
            logging.error(f"Error in summarize_whitepaper: {str(e)}")
            return f"Error analyzing whitepaper for {crypto_input}: {str(e)}"

    def generate_advice(self, crypto_input, previous_analyses=None, **kwargs):
        """Enhanced advice generation with comprehensive analysis synthesis"""
        if previous_analyses:
            advice_prompt = f"""
As a professional cryptocurrency trading advisor, provide comprehensive trading advice for {crypto_input}.

I have already conducted thorough research on this cryptocurrency. Here are the findings:

**WHITEPAPER ANALYSIS:**
{previous_analyses.get('whitepaper', 'No whitepaper analysis available')}

**REDDIT SENTIMENT ANALYSIS:**
{previous_analyses.get('sentiment', {}).get('analysis', 'No sentiment analysis available')}

**LATEST NEWS ANALYSIS:**
{previous_analyses.get('news', {}).get('analysis', 'No news analysis available')}

**TECHNICAL ANALYSIS:**
{previous_analyses.get('technical', {}).get('analysis', 'No technical analysis available')}

Based on ALL of this comprehensive research, provide:

**SYNTHESIS & OVERVIEW:**
- How do the whitepaper fundamentals, sentiment, news, and technical analysis align?
- What is the overall picture for {crypto_input}?

**TRADING RECOMMENDATION:**
- Clear Buy/Sell/Hold recommendation with reasoning from all sources
- Position size suggestion (conservative/moderate/aggressive)
- Confidence level based on alignment of all analyses

**STRATEGY:**
- Entry points considering technical levels and sentiment
- Exit strategy based on technical resistance and fundamental outlook
- Timeline considerations from news and project developments

**RISK ASSESSMENT:**
- Risks identified from sentiment, news, and technical analysis
- How project fundamentals affect long-term vs short-term outlook

**DISCLAIMER:** Include that this is educational content only and not financial advice.
"""
        else:
            advice_prompt = f"""
As a professional cryptocurrency trading advisor, provide comprehensive trading advice for {crypto_input}.

Please follow this process:
1. First, gather current price data and market metrics
2. Then, search for recent news and developments
3. Next, check Reddit for community sentiment
4. Finally, search for whitepaper/technical information if needed

Based on your research, provide:

**MARKET OVERVIEW:**
- Current price and recent performance
- Market position and key metrics

**SENTIMENT ANALYSIS:**
- Community mood and discussions
- Recent news impact

**TRADING RECOMMENDATION:**
- Clear Buy/Sell/Hold recommendation with reasoning
- Position size suggestion (conservative/moderate/aggressive)
- Confidence level and risk assessment

**STRATEGY:**
- Entry points and price targets
- Stop-loss recommendations
- Timeline considerations

**DISCLAIMER:** Include that this is educational content only and not financial advice.
"""
        try:
            result = self.agent_executor.invoke({"input": advice_prompt})
            return {
                "advice": result.get("output", f"No trading advice available for {crypto_input}"),
                "intermediate_steps": result.get("intermediate_steps", []),
                "success": True
            }
        except Exception as e:
            logging.error(f"Error generating advice: {e}")
            return {
                "advice": f"Error generating advice for {crypto_input}: {str(e)}",
                "intermediate_steps": [],
                "success": False
            }