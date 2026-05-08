import streamlit as st
from kiteconnect import KiteConnect
import pandas as pd
import time
import random
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Pro AI Trader Terminal", layout="wide")

# Custom CSS for Dark Fintech Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetricValue"] { font-size: 24px; color: #00ffcc; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #262730; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Pro AI Trading Terminal")

# --- Sidebar ---
st.sidebar.header("🕹️ Control Panel")
demo_mode = st.sidebar.toggle("Demo Mode (Fake Data)", value=True)

# Session State for Logs & Data
if 'trade_log' not in st.session_state: st.session_state.trade_log = []
if 'price_history' not in st.session_state: st.session_state.price_history = pd.DataFrame(columns=['Time', 'Price', 'Open', 'High', 'Low', 'Close'])

# --- Top Row: Multi-Index Watchlist ---
cols = st.columns(4)
indices = ["NIFTY 50", "BANKNIFTY", "FINNIFTY", "INDIA VIX"]
for i, index in enumerate(indices):
    with cols[i]:
        val = random.randint(20000, 24000) if demo_mode else 0 # Real logic here
        st.metric(index, f"₹{val}", f"{random.uniform(-1, 1):.2f}%")

st.divider()

# --- Main Layout: Chart & AI Analysis ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Live Candlestick Analysis")
    
    # Generating Mock Candlestick Data
    curr_p = st.session_state.price_history['Price'].iloc[-1] if not st.session_state.price_history.empty else 24200
    new_p = curr_p + random.randint(-20, 20)
    
    new_row = {'Time': datetime.now().strftime('%H:%M:%S'), 'Price': new_p, 
               'Open': curr_p, 'High': max(curr_p, new_p) + 5, 'Low': min(curr_p, new_p) - 5, 'Close': new_p}
    
    st.session_state.price_history = pd.concat([st.session_state.price_history, pd.DataFrame([new_row])], ignore_index=True)
    if len(st.session_state.price_history) > 30: st.session_state.price_history = st.session_state.price_history.iloc[1:]

    # Plotly Candlestick Chart
    fig = go.Figure(data=[go.Candlestick(x=st.session_state.price_history['Time'],
                open=st.session_state.price_history['Open'],
                high=st.session_state.price_history['High'],
                low=st.session_state.price_history['Low'],
                close=st.session_state.price_history['Close'],
                increasing_line_color= '#00ffcc', decreasing_line_color= '#ff4b4b')])
    
    fig.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=10, b=10), height=400)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🧠 AI Signal Center")
    
    # Confidence Score Simulation
    conf = random.randint(40, 95)
    st.write(f"**AI Confidence:** {conf}%")
    st.progress(conf / 100)
    
    # Signal Box
    if conf > 75:
        st.success("🚀 SIGNAL: STRONG BUY")
        if st.button("Execute BUY Order"):
            st.session_state.trade_log.append(f"[{datetime.now().strftime('%H:%M')}] Bought NIFTY at {new_p}")
    elif conf < 50:
        st.error("📉 SIGNAL: STRONG SELL")
        if st.button("Execute SELL Order"):
            st.session_state.trade_log.append(f"[{datetime.now().strftime('%H:%M')}] Sold NIFTY at {new_p}")
    else:
        st.warning("⏳ SIGNAL: WAIT / SIDEWAYS")

    # Trade Log
    st.write("---")
    st.write("**Recent Activity Log**")
    for log in reversed(st.session_state.trade_log[-5:]):
        st.caption(log)

# Auto-refresh
time.sleep(2)
st.rerun()
