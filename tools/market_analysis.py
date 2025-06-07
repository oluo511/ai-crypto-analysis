def analyze_news_headlines(headlines):
    """
    Analyze a list of news headlines to detect bullish or bearish tone.
    
    Args:
        headlines (list): List of dicts with 'title' and/or 'snippet'

    Returns:
        dict: {
            'bullish': [...],
            'bearish': [...],
            'neutral': [...]
        }
    """
    bullish_keywords = ["rally", "surge", "breakout", "bullish", "gain", "pump", "buy"]
    bearish_keywords = ["crash", "dip", "bearish", "sell-off", "drop", "dump", "retrace"]

    summary = {"bullish": [], "bearish": [], "neutral": []}

    for item in headlines:
        text = f"{item.get('title', '')} {item.get('snippet', '')}".lower()
        if any(word in text for word in bullish_keywords):
            summary["bullish"].append(item)
        elif any(word in text for word in bearish_keywords):
            summary["bearish"].append(item)
        else:
            summary["neutral"].append(item)

    return summary