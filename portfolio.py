import json
from pathlib import Path

PORTFOLIO_FILE = Path(__file__).parent / "portfolio.json"


def load_portfolio() -> dict:
    """Load holdings from disk. Returns empty dict if no file exists yet."""
    if PORTFOLIO_FILE.exists():
        return json.loads(PORTFOLIO_FILE.read_text())
    return {}


def save_portfolio(portfolio: dict):
    """Persist the portfolio dict to disk as JSON."""
    PORTFOLIO_FILE.write_text(json.dumps(portfolio, indent=2))


def add_holding(ticker: str, shares: float, buy_price: float):
    """Add or overwrite a holding. Ticker is uppercased automatically."""
    portfolio = load_portfolio()
    portfolio[ticker.upper()] = {"shares": shares, "buy_price": buy_price}
    save_portfolio(portfolio)


def remove_holding(ticker: str):
    """Remove a holding by ticker. No-op if it doesn't exist."""
    portfolio = load_portfolio()
    portfolio.pop(ticker.upper(), None)
    save_portfolio(portfolio)
