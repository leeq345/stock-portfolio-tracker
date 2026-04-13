import yfinance as yf
from datetime import datetime


def get_stock_data(tickers: list) -> dict:
    """
    Fetch current price, previous close, and day change % for a list of tickers.
    Returns a dict: { "AAPL": { current_price, prev_close, day_change_pct }, ... }
    Tickers that fail (invalid symbol, network error) are skipped.
    """
    results = {}
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).fast_info
            price = info.last_price
            prev = info.previous_close
            if price and prev:
                results[ticker] = {
                    "current_price": round(price, 2),
                    "prev_close": round(prev, 2),
                    "day_change_pct": round(((price - prev) / prev) * 100, 2),
                }
        except Exception:
            pass
    return results


def get_news(ticker: str, max_articles: int = 3) -> list:
    """
    Fetch the latest news headlines for a ticker via yfinance.
    Returns a list of dicts: { title, link, publisher, published_at }
    Returns an empty list if news is unavailable.
    """
    try:
        raw = yf.Ticker(ticker).news or []
        articles = []
        for item in raw[:max_articles]:
            # yfinance nests article data under a 'content' key in newer versions
            content = item.get("content", item)
            title = content.get("title", "No title")
            link = (
                content.get("canonicalUrl", {}).get("url")
                or content.get("clickThroughUrl", {}).get("url")
                or content.get("link", "#")
            )
            publisher = (
                content.get("provider", {}).get("displayName")
                or content.get("publisher", "Unknown")
            )
            timestamp = content.get("pubDate") or content.get("providerPublishTime")
            if isinstance(timestamp, (int, float)):
                published_at = datetime.fromtimestamp(timestamp).strftime("%b %d, %Y")
            elif isinstance(timestamp, str):
                published_at = timestamp[:10]
            else:
                published_at = ""
            articles.append({
                "title": title,
                "link": link,
                "publisher": publisher,
                "published_at": published_at,
            })
        return articles
    except Exception:
        return []
