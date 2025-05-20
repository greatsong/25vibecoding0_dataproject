import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="글로벌 시가총액 Top 10 주가 변동")

st.title("🌍 글로벌 시가총액 Top 10 기업의 최근 1년 주가 변동")

top10 = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "Nvidia": "NVDA",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "Eli Lilly": "LLY",
    "TSMC": "TSM"
}

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

st.info("데이터를 불러오는 중입니다. 잠시만 기다려주세요...")

# 여러 티커를 동시에 받을 경우 MultiIndex 컬럼이 됨
raw_data = yf.download(list(top10.values()), start=start_date, end=end_date)

# 'Adj Close' 레벨만 뽑아오기 (종목별 단일 인덱스)
data = raw_data['Adj Close']

fig = go.Figure()

for name, ticker in top10.items():
    if ticker in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[ticker],
            mode='lines',
            name=name
        ))
    else:
        st.warning(f"{name} ({ticker}) 데이터가 없습니다.")

fig.update_layout(
    title="글로벌 시가총액 Top 10 기업 최근 1년 주가 변동 (Adj Close)",
    xaxis_title="날짜",
    yaxis_title="주가 (USD 또는 현지 통화)",
    legend_title="기업명",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.caption("""
시가총액 기준 상위 10개 글로벌 기업의 최근 1년 주가 변동을 한눈에 볼 수 있습니다.  
*데이터는 Yahoo Finance 제공.  
(참고: 사우디 아람코(2222.SR)는 리얄 단위, TSMC는 대만증시 단위)  
""")
