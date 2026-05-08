import streamlit as st
from kiteconnect import KiteConnect
import pandas as pd
import time
import random

st.set_page_config(page_title="AI Trader Pro", layout="wide")
st.title("🚀 My AI Trading Dashboard")

# Sidebar
st.sidebar.header("Settings")
demo_mode = st.sidebar.checkbox("Demo Mode (Bina API ke chalayein)", value=True)

if not demo_mode:
    api_key = st.sidebar.text_input("Enter Kite API Key")
    access_token = st.sidebar.text_input("Enter Today's Access Token", type="password")
else:
    st.sidebar.info("Demo Mode On hai. Fake data dikh raha hai.")
    api_key = "demo"
    access_token = "demo"

if api_key and access_token:
    try:
        if demo_mode:
            # Fake Data for Demo
            price = 24250 + random.randint(-50, 50)
            rsi = random.randint(30, 70)
        else:
            # Real Zerodha Connection
            kite = KiteConnect(api_key=api_key)
            kite.set_access_token(access_token)
            price = kite.ltp("NSE:NIFTY 50")["NSE:NIFTY 50"]["last_price"]
            rsi = 55 # placeholder

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="NIFTY 50 Live", value=f"₹{price}")
        with col2:
            if rsi > 60:
                st.success(f"🎯 SIGNAL: BUY (RSI: {rsi})")
            elif rsi < 40:
                st.error(f"🎯 SIGNAL: SELL (RSI: {rsi})")
            else:
                st.warning(f"🎯 SIGNAL: WAIT (RSI: {rsi})")

        if 'data_list' not in st.session_state:
            st.session_state.data_list = []
        st.session_state.data_list.append(price)
        if len(st.session_state.data_list) > 20:
            st.session_state.data_list.pop(0)
            
        st.line_chart(st.session_state.data_list)
        time.sleep(2)
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")
