import streamlit as st
import pandas as pd
import plotly.express as px
from portfolio import load_portfolio, add_holding, remove_holding
from stocks import get_stock_data, get_news

# Popular tech stocks to watch for positive trading alerts
TECH_WATCHLIST = [
    "AAPL", "MSFT", "GOOGL", "META", "NVDA",
    "TSLA", "AMZN", "AMD", "INTC", "CRM",
]

st.set_page_config(page_title="Stock Portfolio Tracker", page_icon="📈", layout="wide")
st.title("📈 Stock Portfolio Tracker")

# ── Sidebar: add / remove holdings ──────────────────────────────────────────
with st.sidebar:
    st.header("Manage Holdings")

    st.subheader("Add a Stock")
    ticker_input = st.text_input("Ticker Symbol", placeholder="e.g. AAPL").upper().strip()
    shares_input = st.number_input("Number of Shares", min_value=0.01, step=0.01, format="%.2f")
    buy_price_input = st.number_input("Buy Price per Share ($)", min_value=0.01, step=0.01, format="%.2f")

    if st.button("Add to Portfolio", use_container_width=True):
        if ticker_input:
            add_holding(ticker_input, shares_input, buy_price_input)
            st.success(f"{ticker_input} added!")
            st.rerun()
        else:
            st.warning("Please enter a ticker symbol.")

    st.divider()

    portfolio = load_portfolio()
    if portfolio:
        st.subheader("Remove a Stock")
        remove_ticker = st.selectbox("Select holding to remove", list(portfolio.keys()))
        if st.button("Remove", use_container_width=True):
            remove_holding(remove_ticker)
            st.success(f"{remove_ticker} removed.")
            st.rerun()

    st.divider()
    if st.button("🔄 Refresh Prices", use_container_width=True):
        st.rerun()

# ── Load portfolio data ──────────────────────────────────────────────────────
portfolio = load_portfolio()

# ── Portfolio section ────────────────────────────────────────────────────────
st.subheader("My Portfolio")

if not portfolio:
    st.info("No holdings yet. Add a stock using the sidebar to get started.")
else:
    tickers = list(portfolio.keys())
    stock_data = get_stock_data(tickers)

    rows = []
    total_value = 0.0
    total_cost = 0.0

    for ticker, holding in portfolio.items():
        data = stock_data.get(ticker)
        if not data:
            rows.append({
                "Ticker": ticker,
                "Shares": holding["shares"],
                "Buy Price": f"${holding['buy_price']:.2f}",
                "Current Price": "N/A",
                "Total Value": "N/A",
                "P&L ($)": "N/A",
                "P&L (%)": "N/A",
            })
            continue

        shares = holding["shares"]
        buy_price = holding["buy_price"]
        current_price = data["current_price"]
        value = current_price * shares
        cost = buy_price * shares
        pnl = value - cost
        pnl_pct = (pnl / cost) * 100

        total_value += value
        total_cost += cost

        rows.append({
            "Ticker": ticker,
            "Shares": shares,
            "Buy Price": f"${buy_price:.2f}",
            "Current Price": f"${current_price:.2f}",
            "Total Value": f"${value:,.2f}",
            "P&L ($)": f"{pnl:+,.2f}",
            "P&L (%)": f"{pnl_pct:+.2f}%",
        })

    # Summary metrics
    total_pnl = total_value - total_cost
    total_pnl_pct = (total_pnl / total_cost * 100) if total_cost else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Portfolio Value", f"${total_value:,.2f}")
    col2.metric("Total Cost Basis", f"${total_cost:,.2f}")
    col3.metric("Total P&L", f"${total_pnl:+,.2f}", f"{total_pnl_pct:+.2f}%")

    st.divider()

    # Side-by-side: portfolio table (left) + allocation pie chart (right)
    col_table, col_chart = st.columns([3, 2])

    with col_table:
        df = pd.DataFrame(rows)

        def color_pnl(val):
            if isinstance(val, str) and val.startswith("+"):
                return "color: #2ecc71; font-weight: bold"
            elif isinstance(val, str) and val.startswith("-"):
                return "color: #e74c3c; font-weight: bold"
            return ""

        styled = df.style.map(color_pnl, subset=["P&L ($)", "P&L (%)"])
        st.dataframe(styled, use_container_width=True, hide_index=True)

    with col_chart:
        # Only include tickers where we have a live price
        chart_data = [
            {"Ticker": r["Ticker"], "Value": stock_data[r["Ticker"]]["current_price"] * portfolio[r["Ticker"]]["shares"]}
            for r in rows
            if r["Current Price"] != "N/A"
        ]
        if chart_data:
            fig = px.pie(
                chart_data,
                names="Ticker",
                values="Value",
                title="Portfolio Allocation",
                hole=0.4,  # donut style
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(showlegend=False, margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

# ── News Feed ────────────────────────────────────────────────────────────────
st.divider()
st.subheader("📰 Latest News")

if not portfolio:
    st.info("Add holdings to see stock news.")
else:
    for ticker in portfolio:
        articles = get_news(ticker)
        with st.expander(f"{ticker} — latest headlines"):
            if not articles:
                st.write("No news available.")
            for article in articles:
                st.markdown(f"**[{article['title']}]({article['link']})**")
                st.caption(f"{article['publisher']}  ·  {article['published_at']}")
                st.write("")

# ── Tech Stock Alerts ────────────────────────────────────────────────────────
st.divider()
st.subheader("🔔 Tech Stock Alerts")
st.caption("Tracking: " + " · ".join(TECH_WATCHLIST))

tech_data = get_stock_data(TECH_WATCHLIST)

positive = {t: d for t, d in tech_data.items() if d and d["day_change_pct"] > 0}
negative = {t: d for t, d in tech_data.items() if d and d["day_change_pct"] <= 0}

if positive:
    st.success(f"**{len(positive)} tech stock(s) trading positive today**")
    cols = st.columns(len(positive))
    for i, (ticker, data) in enumerate(sorted(positive.items(), key=lambda x: -x[1]["day_change_pct"])):
        with cols[i]:
            st.metric(
                label=ticker,
                value=f"${data['current_price']:.2f}",
                delta=f"{data['day_change_pct']:+.2f}%",
            )

if negative:
    with st.expander(f"📉 {len(negative)} stock(s) trading flat or negative"):
        cols = st.columns(min(len(negative), 5))
        for i, (ticker, data) in enumerate(sorted(negative.items(), key=lambda x: x[1]["day_change_pct"])):
            with cols[i % 5]:
                st.metric(
                    label=ticker,
                    value=f"${data['current_price']:.2f}",
                    delta=f"{data['day_change_pct']:+.2f}%",
                )
