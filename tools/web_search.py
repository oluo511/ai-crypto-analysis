import os
import time
import json
import logging
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class WebSearch:
    def __init__(self, api_key=None, cooldown=None):
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        self.cooldown = cooldown or int(os.getenv("SERPER_COOLDOWN", 60))
        self.last_request_time = 0
        self.serper_url = "https://google.serper.dev/search"

        # Validate API Key
        if not self.api_key:
            raise ValueError("⚠️ SERPER_API_KEY not found. Make sure it is set in your .env file.")
        
        logging.info("✅ Serper API configuration initialized successfully.")

    def _rate_limit(self):
        elapsed_time = time.time() - self.last_request_time
        if elapsed_time < self.cooldown:
            wait_time = self.cooldown - elapsed_time
            logging.info(f"⏳ Rate limit reached. Waiting for {wait_time:.2f} seconds...")
            time.sleep(wait_time)

    def search_whitepaper(self, project_name_or_symbol, num_results=5):
        self._rate_limit()

        try:
            # Formulate the search query
            query = f"{project_name_or_symbol} white paper"
            print(f"Sending query: '{query}'")
            
            # Make direct API request to Serper instead of using wrapper
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": query,
                "gl": "us",
                "hl": "en",
                "num": num_results
            }
            
            response = requests.post(self.serper_url, headers=headers, json=payload)
            
            # Debug output
            print(f"Response status code: {response.status_code}")
            
            # Check if request was successful
            if response.status_code != 200:
                logging.error(f"⚠️ API request failed with status code {response.status_code}: {response.text}")
                return {"error": f"API request failed with status code {response.status_code}"}
            
            # Parse JSON response
            try:
                results = response.json()
                print(f"Results structure keys: {list(results.keys())}")
            except json.JSONDecodeError as e:
                logging.error(f"⚠️ Failed to decode JSON response: {e}")
                print(f"Response content: {response.text[:500]}...")  # Print first 500 chars
                return {"error": f"Failed to decode JSON response: {e}"}
            
            # Extract relevant information
            extracted_results = []
            
            # Process organic results
            if "organic" in results:
                for item in results["organic"][:num_results]:
                    extracted_results.append({
                        "title": item.get("title", "No title"),
                        "snippet": item.get("snippet", "No snippet"),
                        "link": item.get("link", "No link")
                    })
            
            # Process knowledge graph results if available and needed
            if "knowledgeGraph" in results and not extracted_results:
                kg = results["knowledgeGraph"]
                extracted_results.append({
                    "title": kg.get("title", "Knowledge Graph"),
                    "snippet": kg.get("description", "No description"),
                    "link": kg.get("website", "No link")
                })
            
            self.last_request_time = time.time()
            logging.info(f"✅ Successfully fetched {len(extracted_results)} results for project: {project_name_or_symbol}")
            return extracted_results

        except Exception as e:
            logging.error(f"⚠️ API Error: {e}")
            return {"error": str(e)}
        
    def search(self, query, num_results=5):
        self._rate_limit()

        try:
            print(f"Sending query: '{query}'")

            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }

            payload = {
                "q": query,
                "gl": "us",
                "hl": "en",
                "num": num_results
            }

            response = requests.post(self.serper_url, headers=headers, json=payload)
            print(f"Response status code: {response.status_code}")

            if response.status_code != 200:
                logging.error(f"⚠️ API request failed with status code {response.status_code}: {response.text}")
                return {"error": f"API request failed with status code {response.status_code}"}

            try:
                results = response.json()
                print(f"Results structure keys: {list(results.keys())}")
            except json.JSONDecodeError as e:
                logging.error(f"⚠️ Failed to decode JSON response: {e}")
                print(f"Response content: {response.text[:500]}...")
                return {"error": f"Failed to decode JSON response: {e}"}

            extracted_results = []

            if "organic" in results:
                for item in results["organic"][:num_results]:
                    extracted_results.append({
                        "title": item.get("title", "No title"),
                        "snippet": item.get("snippet", "No snippet"),
                        "link": item.get("link", "No link")
                    })

            if "knowledgeGraph" in results and not extracted_results:
                kg = results["knowledgeGraph"]
                extracted_results.append({
                    "title": kg.get("title", "Knowledge Graph"),
                    "snippet": kg.get("description", "No description"),
                    "link": kg.get("website", "No link")
                })

            self.last_request_time = time.time()
            logging.info(f"✅ Successfully fetched {len(extracted_results)} results for: {query}")
            return extracted_results

        except Exception as e:
            logging.error(f"⚠️ API Error: {e}")
            return {"error": str(e)}
        
    def search_reddit_sentiment(self, asset, num_results=8):
        """Search Reddit for sentiment about cryptocurrency - FIXED INDENTATION"""
        try:
            # Target crypto subreddits
            crypto_subreddits = [
                "r/CryptoCurrency", "r/CryptoMarkets", "r/altcoin",
                "r/defi", "r/CryptoMoonShots", f"r/{asset.lower()}"
            ]

            subreddit_sites = " OR ".join([f"site:reddit.com/{sub}" for sub in crypto_subreddits])
            query = f"{asset} ({subreddit_sites})"

            logging.info(f"Starting Reddit sentiment search for: {asset}")
            raw_results = self.search(query, num_results=num_results)

            if isinstance(raw_results, dict) and "error" in raw_results:
                logging.error(f"Reddit search error: {raw_results['error']}")
                return {"error": raw_results["error"]}

            # Classify sentiment based on keywords
            positive, neutral, negative = [], [], []

            # Enhanced keyword lists
            positive_keywords = [
                "bullish", "buy", "moon", "pump", "surge", "rocket", 
                "hodl", "diamond hands", "to the moon", "bullrun", 
                "rally", "breakout", "long", "accumulating"
            ]
            
            negative_keywords = [
                "scam", "dump", "bearish", "crash", "loss", "lawsuit", 
                "rugpull", "dead", "rip", "sell", "short", "bubble", 
                "overvalued", "avoid", "disaster"
            ]

            for post in raw_results:
                title = post.get("title", "").lower()
                snippet = post.get("snippet", "").lower()
                text = f"{title} {snippet}"

                # Count positive and negative sentiment
                pos_count = sum(1 for word in positive_keywords if word in text)
                neg_count = sum(1 for word in negative_keywords if word in text)

                if pos_count > neg_count and pos_count > 0:
                    positive.append(post)
                elif neg_count > pos_count and neg_count > 0:
                    negative.append(post)
                else:
                    neutral.append(post)

            total_posts = len(positive) + len(neutral) + len(negative)
            logging.info(f"✅ Reddit sentiment complete for {asset}: {len(positive)} positive, {len(negative)} negative, {len(neutral)} neutral (total: {total_posts})")

            return {
                "positive": positive,
                "neutral": neutral,
                "negative": negative
            }
            
        except Exception as e:
            logging.error(f"Error in search_reddit_sentiment: {str(e)}")
            return {"error": f"Reddit sentiment search failed: {str(e)}"}

    def search_latest_news(self, asset, num_results=5):
        """Search for latest cryptocurrency news"""
        # More specific crypto news search
        query = f'"{asset}" cryptocurrency news OR "{asset}" crypto news OR "{asset}" token news'
        return self.search(query, num_results=num_results)