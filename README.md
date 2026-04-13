# Stock Portfolio Tracker

A simple web-based stock portfolio tracker built with Streamlit and yfinance.

## Features

- 📈 Add and track your stock holdings (ticker, shares, buy price)
- 💰 View live prices, P&L, and portfolio allocation
- 📊 Interactive donut chart showing portfolio allocation by value
- 📰 Latest news headlines for each stock in your portfolio
- 🔔 Tech stock alerts - see which stocks are trading positive today

## Tech Stack

- **Python 3.10+**
- **Streamlit** - web dashboard
- **yfinance** - live stock data (free, no API key needed)
- **Plotly** - interactive charts
- **Pandas** - data manipulation

## Installation

1. Clone the repo:
```bash
git clone https://github.com/YOUR_USERNAME/stock-portfolio-tracker.git
cd stock-portfolio-tracker
Install dependencies:

pip install -r requirements.txt
Run the app:

streamlit run app.py
The app will open at http://localhost:8501

## Usage

Add a Stock - Enter a ticker symbol (e.g. AAPL), number of shares, and buy price in the sidebar
View Portfolio - See your holdings, current prices, and P&L
Check Allocation - View the donut chart showing how your money is distributed
Read News - Click any stock to expand its latest headlines
Monitor Tech Stocks - See which tech stocks are up today in the alerts section
File Structure

stock-portfolio-tracker/
├── app.py              # Main Streamlit dashboard
├── stocks.py           # yfinance data fetching
├── portfolio.py        # Portfolio save/load (JSON)
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md



---


