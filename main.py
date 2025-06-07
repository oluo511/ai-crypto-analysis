from agents.analyst import CryptoAnalysisAgent
from agents.technical_analyst import TechnicalAnalysisAgent
from tools.web_search import WebSearch
import logging

# Set up logging to see agent reasoning
logging.basicConfig(level=logging.INFO)

def test_web_search():
    """Test the basic WebSearch functionality"""
    print("\n" + "="*50)
    print("🔄 Testing WebSearch Tools...")
    print("="*50)
    
    web_search = WebSearch()
    
    # Test whitepaper search
    print("\n📄 Testing Whitepaper Search:")
    search_results = web_search.search_whitepaper("Bitcoin", num_results=3)
    
    if isinstance(search_results, dict) and "error" in search_results:
        print(f"❌ Error: {search_results['error']}")
    else:
        for i, result in enumerate(search_results[:3], 1):
            print(f"{i}. {result.get('title', 'No title')}")
            print(f"   {result.get('snippet', 'No snippet')[:100]}...")
            print(f"   🔗 {result.get('link', 'No link')}")
    
    # Test Reddit sentiment search
    print("\n💬 Testing Reddit Sentiment Search:")
    reddit_results = web_search.search_reddit_sentiment("Bitcoin", num_results=3)
    
    if isinstance(reddit_results, dict) and "error" in reddit_results:
        print(f"❌ Error: {reddit_results['error']}")
    else:
        for i, result in enumerate(reddit_results[:3], 1):
            print(f"{i}. {result.get('title', 'No title')}")
            print(f"   {result.get('snippet', 'No snippet')[:100]}...")

def test_langchain_agent():
    """Test the LangChain-based CryptoAnalysisAgent"""
    print("\n" + "="*50)
    print("🤖 Testing LangChain CryptoAnalysisAgent...")
    print("="*50)
    
    try:
        # Initialize agent
        agent = CryptoAnalysisAgent()
        print("✅ Agent initialized successfully")
        
        # Test focused trading advice
        print("\n🎯 Testing Focused Trading Advice for Bitcoin:")
        print("-" * 30)
        
        advice_result = agent.get_focused_advice("Bitcoin")
        
        if advice_result["success"]:
            print("✅ Trading advice generated successfully!")
            print("\n📋 Advice Preview:")
            print(advice_result["advice"][:500] + "..." if len(advice_result["advice"]) > 500 else advice_result["advice"])
            
            print(f"\n🔍 Agent used {len(advice_result['intermediate_steps'])} tool calls")
            for i, step in enumerate(advice_result['intermediate_steps'][:3], 1):
                action = step[0]
                print(f"Step {i}: Used tool '{getattr(action, 'tool', 'unknown')}'")
        else:
            print(f"❌ Error: {advice_result['advice']}")
        
        # Test comprehensive analysis
        print("\n📊 Testing Comprehensive Analysis for Ethereum:")
        print("-" * 30)
        
        comprehensive_result = agent.analyze_cryptocurrency("Ethereum", ["price", "news", "advice"])
        
        if comprehensive_result["success"]:
            print("✅ Comprehensive analysis completed!")
            print("\n📋 Analysis Preview:")
            print(comprehensive_result["analysis"][:400] + "..." if len(comprehensive_result["analysis"]) > 400 else comprehensive_result["analysis"])
        else:
            print(f"❌ Error: {comprehensive_result['analysis']}")
            
    except Exception as e:
        print(f"❌ Error testing LangChain agent: {e}")

def test_technical_agent():
    """Test the Technical Analysis Agent"""
    print("\n" + "="*50)
    print("📊 Testing Technical Analysis Agent...")
    print("="*50)
    
    try:
        # Initialize technical agent
        tech_agent = TechnicalAnalysisAgent()
        print("✅ Technical agent initialized successfully")
        
        # Test technical analysis
        print("\n📈 Testing Technical Analysis for Bitcoin:")
        print("-" * 30)
        
        tech_result = tech_agent.perform_technical_analysis("Bitcoin")
        
        if "error" not in tech_result:
            print("✅ Technical analysis completed!")
            print(f"\n💰 Current Price: ${tech_result['current_price']:,.6f}")
            print(f"📊 RSI: {tech_result['rsi']:.2f}")
            print(f"📈 24h Change: {tech_result['price_changes']['24h']:.2f}%")
            print(f"🎯 Signal: {tech_result['signals']['signal'].upper()}")
            print(f"🔥 Confidence: {tech_result['signals']['confidence']:.0%}")
            
            print("\n🧠 AI Analysis Preview:")
            print(tech_result['analysis'][:300] + "..." if len(tech_result['analysis']) > 300 else tech_result['analysis'])
        else:
            print(f"❌ Error: {tech_result['error']}")
            
    except Exception as e:
        print(f"❌ Error testing technical agent: {e}")

def test_compatibility_methods():
    """Test the compatibility wrapper methods"""
    print("\n" + "="*50)
    print("🔧 Testing Compatibility Methods...")
    print("="*50)
    
    try:
        agent = CryptoAnalysisAgent()
        
        # Test individual methods that Streamlit expects
        print("\n📄 Testing summarize_whitepaper:")
        whitepaper = agent.summarize_whitepaper("Solana")
        print("✅ Whitepaper analysis:", whitepaper[:150] + "..." if len(whitepaper) > 150 else whitepaper)
        
        print("\n💬 Testing analyze_sentiment:")
        sentiment = agent.analyze_sentiment("Solana")
        print("✅ Sentiment analysis completed")
        
        print("\n📰 Testing analyze_news_headlines:")
        news = agent.analyze_news_headlines("Solana")
        print("✅ News analysis completed")
        
        print("\n🎯 Testing generate_advice:")
        advice = agent.generate_advice("Solana")
        print("✅ Advice generation:", advice[:150] + "..." if len(advice) > 150 else advice)
        
    except Exception as e:
        print(f"❌ Error testing compatibility methods: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Crypto Analysis Agent Tests")
    print("=" * 60)
    
    # Test basic web search functionality
    test_web_search()
    
    # Test LangChain agent
    test_langchain_agent()
    
    # Test technical analysis agent
    test_technical_agent()
    
    # Test compatibility methods for Streamlit
    test_compatibility_methods()
    
    print("\n" + "="*60)
    print("✅ All Tests Complete!")
    print("🎯 If everything worked, your Streamlit app should work too!")
    print("📝 Run: streamlit run app.py")
    print("="*60)

if __name__ == "__main__":
    main()