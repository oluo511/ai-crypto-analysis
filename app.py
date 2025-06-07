import streamlit as st
from agents.analyst import CryptoAnalysisAgent
from agents.technical_analyst import TechnicalAnalysisAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Page config
st.set_page_config(
    page_title="Crypto Analysis",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(40, 44, 52, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card {
        background: rgba(40, 44, 52, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(55, 60, 70, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    .success-box {
        background: rgba(40, 44, 52, 0.7);
        border: 1px solid rgba(72, 187, 120, 0.3);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: rgba(40, 44, 52, 0.7);
        border: 1px solid rgba(255, 107, 107, 0.3);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .info-box {
        background: rgba(40, 44, 52, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .error-box {
        background: rgba(40, 44, 52, 0.7);
        border: 1px solid rgba(255, 107, 107, 0.5);
        padding: 1rem;
        border-radius: 10px;
        color: #ff6b6b;
        margin: 1rem 0;
    }
            
    .stButton > button {
        background: rgba(139, 92, 246, 0.8) !important;
        border: 1px solid rgba(139, 92, 246, 1) !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: rgba(139, 92, 246, 1) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3) !important;
    }
            
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, rgba(139, 92, 246, 0.8), rgba(139, 92, 246, 1)) !important;
    }

    div[data-testid="stProgress"] > div > div > div > div {
        background: rgba(139, 92, 246, 1) !important;
    }
    
    .disclaimer-footer {
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid rgba(255, 107, 107, 0.3);
        padding: 1rem;
        border-radius: 10px;
        color: #ff6b6b;
        margin: 1rem 0;
        font-size: 0.9rem;
        text-align: center;
    }

    .stTabs [data-baseweb="tab-list"] {
        width: 100%;
        display: flex;
        justify-content: space-evenly;
        gap: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        text-align: center;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        background: rgba(40, 44, 52, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 8px 8px 0 0 !important;
        margin: 0 2px !important;
        min-height: 60px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(55, 60, 70, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(139, 92, 246, 0.8) !important;
        border: 1px solid rgba(139, 92, 246, 1) !important;
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(40, 44, 52, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0 0 8px 8px !important;
        padding: 2rem !important;
        min-height: 400px !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Crypto Analysis</h1>
    <p>AI-powered cryptocurrency analysis with sentiment insights and trading suggestions</p>
</div>
""", unsafe_allow_html=True)

# Main content area - always show cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>📊 Market Analysis</h3>
        <p>Get comprehensive market insights and technical analysis</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>💭 Sentiment Tracking</h3>
        <p>Monitor social media sentiment from Reddit discussions</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>📊 Technical Analysis</h3>
        <p>RSI, MACD, Bollinger Bands, and trading signals</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3>🎯 Trading Advice</h3>
        <p>Receive AI-generated trading recommendations</p>
    </div>
    """, unsafe_allow_html=True)

# Centered search below cards
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Feature selection FIRST
    st.markdown("""
    <div style='margin: 1rem 0; text-align: center;'>
        <h4>Select analysis types:</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    with col_a:
        show_whitepaper = st.checkbox("📄 Whitepaper", value=True)
    with col_b:
        show_sentiment = st.checkbox("💬 Sentiment", value=True)  
    with col_c:
        show_news = st.checkbox("📰 News", value=True)
    with col_d:
        show_technical = st.checkbox("📊 Technical", value=True)
    with col_e:
        show_advice = st.checkbox("🎯 Advice", value=True)
    
    # Search input
    crypto_input = st.text_input(
        "",
        placeholder="Enter cryptocurrency name (e.g., Bitcoin, Ethereum, Solana...)",
    )
    
    analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)

# Helper function to safely display results
def safe_display_content(content, title="Content"):
    """Safely display content with proper error handling"""
    if not content:
        st.warning(f"No {title.lower()} available.")
        return
    
    if isinstance(content, dict) and 'error' in content:
        st.markdown(f"""
        <div class="error-box">
            ❌ <strong>Error:</strong> {content['error']}
        </div>
        """, unsafe_allow_html=True)
        return
    
    if isinstance(content, str):
        if "error" in content.lower() or "failed" in content.lower():
            st.markdown(f"""
            <div class="warning-box">
                ⚠️ <strong>Issue:</strong> {content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-box">
                {content}
            </div>
            """, unsafe_allow_html=True)

# Run analysis when button clicked
if analyze_button and crypto_input:
    # Initialize session state for results caching
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    
    # Show analysis in progress
    with st.spinner(f"🔍 Analyzing {crypto_input}..."):
        try:
            # Initialize the advisor
            advisor = CryptoAnalysisAgent()
            
            # Initialize technical agent if needed
            technical_agent = None
            if show_technical:
                try:
                    technical_agent = TechnicalAnalysisAgent()
                except Exception as e:
                    st.warning(f"Technical analysis agent failed to initialize: {str(e)}")
                    technical_agent = None
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = {}
            total_steps = sum([show_whitepaper, show_sentiment, show_news, show_technical, show_advice])
            current_step = 0
            
            # Whitepaper Analysis
            if show_whitepaper:
                current_step += 1
                status_text.text("📄 AI Agent analyzing whitepaper...")
                progress_bar.progress(int(current_step / total_steps * 100))
                try:
                    results['whitepaper'] = advisor.summarize_whitepaper(crypto_input)
                except Exception as e:
                    results['whitepaper'] = f"Error analyzing whitepaper: {str(e)}"
                    logging.error(f"Whitepaper analysis error: {e}")
            
            # Sentiment Analysis
            if show_sentiment:
                current_step += 1
                status_text.text("💬 AI Agent analyzing Reddit sentiment...")
                progress_bar.progress(int(current_step / total_steps * 100))
                try:
                    results['sentiment'] = advisor.analyze_sentiment(crypto_input)
                except Exception as e:
                    results['sentiment'] = {
                        'analysis': f"Error analyzing sentiment: {str(e)}",
                        'positive': [],
                        'negative': [],
                        'neutral': []
                    }
                    logging.error(f"Sentiment analysis error: {e}")
            
            # News Analysis
            if show_news:
                current_step += 1
                status_text.text("📰 AI Agent fetching latest news...")
                progress_bar.progress(int(current_step / total_steps * 100))
                try:
                    results['news'] = advisor.analyze_news_headlines(crypto_input)
                except Exception as e:
                    results['news'] = {
                        'analysis': f"Error analyzing news: {str(e)}",
                        'bullish': [],
                        'neutral': [],
                        'bearish': []
                    }
                    logging.error(f"News analysis error: {e}")
            
            # Technical Analysis
            if show_technical and technical_agent:
                current_step += 1
                status_text.text("📊 Performing technical analysis...")
                progress_bar.progress(int(current_step / total_steps * 100))
                try:
                    results['technical'] = technical_agent.perform_technical_analysis(crypto_input)
                except Exception as e:
                    results['technical'] = {
                        'error': f"Technical analysis failed: {str(e)}",
                        'analysis': f"Error performing technical analysis: {str(e)}"
                    }
                    logging.error(f"Technical analysis error: {e}")
            elif show_technical and not technical_agent:
                results['technical'] = {
                    'error': "Technical analysis agent not available",
                    'analysis': "Technical analysis could not be performed due to initialization failure."
                }
            
            # Trading Advice - NOW USES PREVIOUS ANALYSES
            if show_advice:
                current_step += 1
                status_text.text("🎯 AI Agent generating comprehensive trading advice...")
                progress_bar.progress(int(current_step / total_steps * 100))
                try:
                    # Pass all previous analyses to the advice generation
                    results['advice'] = advisor.generate_advice(crypto_input, previous_analyses=results)
                except Exception as e:
                    results['advice'] = {
                        'advice': f"Error generating advice: {str(e)}",
                        'success': False
                    }
                    logging.error(f"Advice generation error: {e}")
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Store results in session state
            st.session_state.analysis_results[crypto_input] = results
            
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            st.exception(e)
            st.stop()
        
    # Display results
    results = st.session_state.analysis_results.get(crypto_input, {})

    st.success(f"✅ Analysis complete for {crypto_input}")

    # Create tabs for different analyses
    tab_names = []
    if show_whitepaper: tab_names.append("📄 Whitepaper")
    if show_sentiment: tab_names.append("💬 Sentiment") 
    if show_news: tab_names.append("📰 News")
    if show_technical: tab_names.append("📊 Technical")
    if show_advice: tab_names.append("🎯 Advice")

    if tab_names:
        tabs = st.tabs(tab_names)
        tab_index = 0
        
        # Whitepaper Tab
        if show_whitepaper and 'whitepaper' in results:
            with tabs[tab_index]:
                st.markdown(f"### 📄 {crypto_input} Whitepaper Summary")
                safe_display_content(results['whitepaper'], "whitepaper analysis")
            tab_index += 1
        
        # Sentiment Tab
        if show_sentiment and 'sentiment' in results:
            with tabs[tab_index]:
                st.markdown(f"### 💬 {crypto_input} Reddit Sentiment Analysis")
                
                sentiment_data = results['sentiment']
                
                if sentiment_data and isinstance(sentiment_data, dict):
                    # Check if we have valid data
                    positive_posts = sentiment_data.get('positive', [])
                    neutral_posts = sentiment_data.get('neutral', [])
                    negative_posts = sentiment_data.get('negative', [])
                    
                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🟢 Positive Posts", len(positive_posts))
                    with col2:
                        st.metric("🟡 Neutral Posts", len(neutral_posts))
                    with col3:
                        st.metric("🔴 Negative Posts", len(negative_posts))

                    # Display analysis summary
                    analysis_text = sentiment_data.get('analysis', 'No analysis available')
                    safe_display_content(analysis_text, "sentiment analysis")

                    # Examples - only show if we have actual posts
                    if positive_posts:
                        st.subheader("🟢 Positive Sentiment Examples:")
                        for post in positive_posts:
                            if isinstance(post, dict) and post.get('title'):
                                st.success(f"**{post.get('title', 'No title')}**\n\n{post.get('snippet', 'No snippet')}")

                    if negative_posts:
                        st.subheader("🔴 Negative Sentiment Examples:")
                        for post in negative_posts:
                            if isinstance(post, dict) and post.get('title'):
                                st.error(f"**{post.get('title', 'No title')}**\n\n{post.get('snippet', 'No snippet')}")
                    
                    if neutral_posts:
                        st.subheader("🟡 Neutral Sentiment Examples:")
                        for post in neutral_posts:
                            if isinstance(post, dict) and post.get('title'):
                                st.warning(f"**{post.get('title', 'No title')}**\n\n{post.get('snippet', 'No snippet')}")
                else:
                    st.warning("Sentiment analysis failed or returned no data.")
            
            tab_index += 1

        # News Tab  
        if show_news and 'news' in results:
            with tabs[tab_index]:
                st.markdown(f"### 📰 {crypto_input} Latest News Analysis")
                
                news_data = results['news']
                
                if news_data and isinstance(news_data, dict):
                    # Check if we have the analysis summary
                    if 'analysis' in news_data:
                        safe_display_content(news_data['analysis'], "news analysis")
                    
                    bullish_articles = news_data.get('bullish', [])
                    neutral_articles = news_data.get('neutral', [])
                    bearish_articles = news_data.get('bearish', [])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🐂 Bullish News", len(bullish_articles))
                    with col2:
                        st.metric("😐 Neutral News", len(neutral_articles))
                    with col3:
                        st.metric("🐻 Bearish News", len(bearish_articles))

                    # Display articles by category
                    for category, articles, emoji in [
                        ('bullish', bullish_articles, '🐂'),
                        ('neutral', neutral_articles, '😐'),
                        ('bearish', bearish_articles, '🐻')
                    ]:
                        if articles:
                            st.subheader(f"{emoji} {category.title()} News:")
                            for article in articles[:5]:
                                if isinstance(article, dict) and article.get('title'):
                                    with st.container():
                                        st.markdown(f"**{article.get('title', 'No title')}**")
                                        if article.get('snippet'):
                                            st.markdown(article.get('snippet', 'No description'))
                                        if article.get('link'):
                                            st.markdown(f"[Read more]({article['link']})")
                                        st.markdown("---")
                else:
                    st.warning("News analysis failed or returned no data.")

            tab_index += 1
        
        # Technical Analysis Tab
        if show_technical and 'technical' in results:
            with tabs[tab_index]:
                st.markdown(f"### 📊 {crypto_input} Technical Analysis")
                
                technical_data = results['technical']
                
                if technical_data and 'error' not in technical_data:
                    # Current Price and Key Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        current_price = technical_data.get('current_price', 0)
                        if current_price:
                            st.metric("💰 Current Price", f"${current_price:.6f}")
                        else:
                            st.metric("💰 Current Price", "N/A")
                    
                    with col2:
                        price_24h = technical_data.get('price_changes', {}).get('24h', 0)
                        if price_24h:
                            st.metric("📈 24h Change", f"{price_24h:.2f}%")
                        else:
                            st.metric("📈 24h Change", "N/A")
                    
                    with col3:
                        rsi = technical_data.get('rsi', 50)
                        if rsi:
                            rsi_color = "🟢" if 30 <= rsi <= 70 else "🔴"
                            st.metric(f"{rsi_color} RSI (14)", f"{rsi:.1f}")
                        else:
                            st.metric("📊 RSI (14)", "N/A")
                    
                    with col4:
                        signals = technical_data.get('signals', {})
                        signal = signals.get('signal', 'hold')
                        confidence = signals.get('confidence', 0)
                        signal_emoji = {"buy": "🟢", "sell": "🔴", "hold": "🟡"}.get(signal, "⚫")
                        if confidence:
                            st.metric(f"{signal_emoji} Signal", signal.upper(), f"{confidence:.0%} confidence")
                        else:
                            st.metric(f"{signal_emoji} Signal", signal.upper())
                    
                    # Technical Indicators
                    st.subheader("📊 Key Technical Indicators")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # MACD
                        macd_data = technical_data.get('macd', {})
                        if macd_data:
                            st.markdown("**MACD Analysis:**")
                            st.write(f"MACD Line: {macd_data.get('macd', 0):.6f}")
                            st.write(f"Signal Line: {macd_data.get('signal', 0):.6f}")
                            st.write(f"Histogram: {macd_data.get('histogram', 0):.6f}")
                        
                        # Support/Resistance
                        sr_data = technical_data.get('support_resistance', {})
                        support_levels = sr_data.get('support', [])
                        if support_levels:
                            st.markdown("**Support Levels:**")
                            for level in support_levels[:3]:
                                st.write(f"${level:.6f}")
                    
                    with col2:
                        # Bollinger Bands
                        bb_data = technical_data.get('bollinger_bands', {})
                        if bb_data:
                            st.markdown("**Bollinger Bands:**")
                            st.write(f"Upper: ${bb_data.get('upper', 0):.6f}")
                            st.write(f"Middle: ${bb_data.get('middle', 0):.6f}")
                            st.write(f"Lower: ${bb_data.get('lower', 0):.6f}")
                        
                        # Resistance
                        resistance_levels = sr_data.get('resistance', [])
                        if resistance_levels:
                            st.markdown("**Resistance Levels:**")
                            for level in resistance_levels[:3]:
                                st.write(f"${level:.6f}")
                    
                    # Trading Signals
                    signals_data = technical_data.get('signals', {})
                    if signals_data.get('reasons'):
                        st.subheader("🎯 Trading Signals")
                        for signal, reason, confidence in signals_data['reasons']:
                            signal_class = {"buy": "🟢", "sell": "🔴", "hold": "🟡"}.get(signal, "⚫")
                            st.markdown(f"**{signal_class} {signal.upper()}**: {reason} (Confidence: {confidence:.0%})")
                    
                    # LLM Analysis
                    if technical_data.get('analysis'):
                        st.subheader("🧠 AI Technical Analysis")
                        safe_display_content(technical_data['analysis'], "technical analysis")
                
                else:
                    # Show error or fallback message
                    error_msg = technical_data.get('error', 'Technical analysis failed or returned no data.')
                    st.markdown(f"""
                    <div class="warning-box">
                        ⚠️ <strong>Technical Analysis Issue:</strong> {error_msg}
                    </div>
                    """, unsafe_allow_html=True)
                
            tab_index += 1
            
        # Advice Tab
        if show_advice and 'advice' in results:
            with tabs[tab_index]:
                st.markdown(f"### 🎯 {crypto_input} Comprehensive Trading Advice")
                
                advice_data = results['advice']
                
                if advice_data:
                    # Check if advice_data is a dict (new format) or string (old format)
                    if isinstance(advice_data, dict):
                        advice_content = advice_data.get('advice', 'No advice available')
                        success = advice_data.get('success', True)
                        
                        if not success:
                            st.markdown(f"""
                            <div class="warning-box">
                                ⚠️ <strong>Advice Generation Issue:</strong> {advice_content}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            safe_display_content(advice_content, "trading advice")
                    else:
                        # Handle string format
                        safe_display_content(advice_data, "trading advice")
                    
                    # Show synthesis indicator
                    analyses_used = []
                    if 'whitepaper' in results: analyses_used.append("📄 Whitepaper")
                    if 'sentiment' in results: analyses_used.append("💬 Sentiment") 
                    if 'news' in results: analyses_used.append("📰 News")
                    if 'technical' in results: analyses_used.append("📊 Technical")
                    
                    if analyses_used:
                        st.markdown(f"""
                        <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3); 
                                   padding: 0.5rem; border-radius: 5px; margin-top: 1rem; font-size: 0.85rem;">
                            <strong>📊 Analysis Sources:</strong> This advice synthesizes insights from: {', '.join(analyses_used)}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Trading advice generation failed or returned no data.")

# Add footer disclaimer
st.markdown("""
<div class="disclaimer-footer">
    ⚠️ <strong>IMPORTANT DISCLAIMER:</strong> This tool provides AI-generated analysis for educational purposes only. 
    This is NOT financial advice. Always do your own research (DYOR) and consult with financial professionals 
    before making any investment decisions. Cryptocurrency trading carries significant risks.
</div>
""", unsafe_allow_html=True)