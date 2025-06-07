# Crypto Analysis Tool

An AI-powered cryptocurrency analysis application built with Streamlit that provides market insights, sentiment analysis, and trading recommendations.

## Features

- Whitepaper analysis using AI
- Reddit sentiment tracking
- Latest news analysis
- Technical analysis with trading signals
- Comprehensive trading recommendations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/oluo511/ai-crypto-analysis.git
cd crypto-analysis-tool
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with your AWS credentials:
```env
aws_access_key_id=your_access_key
aws_secret_access_key=your_secret_key
SERPER_API_KEY=your_secret_key
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Select which analysis types you want (Whitepaper, Sentiment, News, Technical, Advice)
2. Enter a cryptocurrency name (e.g., Bitcoin, Ethereum)
3. Click "Analyze" to run the AI analysis
4. View results in the tabbed interface

## Project Structure

```
├── app.py                      # Main Streamlit application
├── main.py                     # Test file (development/testing purposes)
├── agents/
│   ├── analyst.py              # Main analysis agent
│   └── technical_analyst.py    # Technical analysis
├── tools/
│   ├── web_search.py          # Web scraping utilities
│   ├── market_analysis.py     # Market data processing
│   └── sentiment_analysis.py  # Sentiment tools
└── requirements.txt           # Dependencies
```

## Technologies

- Streamlit (web interface)
- AWS Bedrock/Claude (AI analysis)
- LangChain (agent framework)
- CoinGecko API (price data)

## Disclaimer

This tool is for educational purposes only and does not provide financial advice. Cryptocurrency trading involves significant risk.
