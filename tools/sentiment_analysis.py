from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_reddit_sentiment(posts):
    """
    Analyze sentiment of Reddit posts based on title + snippet.

    Args:
        posts (list): List of dicts with 'title' and 'snippet' keys.

    Returns:
        dict: Categorized sentiment with compound scores.
    """
    sentiment_summary = {
        "positive": [],
        "neutral": [],
        "negative": []
    }

    for post in posts:
        text = f"{post.get('title', '')} {post.get('snippet', '')}".strip()
        score = analyzer.polarity_scores(text)["compound"]

        if score >= 0.05:
            sentiment_summary["positive"].append({**post, "score": score})
        elif score <= -0.05:
            sentiment_summary["negative"].append({**post, "score": score})
        else:
            sentiment_summary["neutral"].append({**post, "score": score})

    return sentiment_summary