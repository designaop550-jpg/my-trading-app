import streamlit as st
from kiteconnect import KiteConnect
import pandas as pd
import time

# --- Dashboard Layout & Style ---
st.set_page_config(page_title="AI Trader Pro", layout="wide")
st.title("🚀 My AI Trading Dashboard")

# --- Sidebar for Keys (Security ke liye) ---
st.sidebar.header("🔑 Zerodha Authentication")
api_key = st.sidebar.text_input("Enter Kite API Key")
access_token = st.sidebar.text_input("Enter Today's Access Token", type="password")

# --- Logic: Agar keys mil jayein toh data dikhao ---
if api_key and access_token:
    try:
        # 1. Zerodha Connection
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)
        
        # 2. Page ko 2 columns mein baantna
        col1, col2 = st.columns(2)
        
        # 3. Nifty 50 ka Live Price lena
        price_data = kite.ltp("NSE:NIFTY 50")
        price = price_data["NSE:NIFTY 50"]["last_price"]
        
        with col1:
            st.metric(label="NIFTY 50 (LIVE)", value=f"₹{price}")
            
        with col2:
            # 4. Simple Signal Logic (Shuruat ke liye placeholder)
            rsi = 55 # Isse baad mein asli RSI se badal denge
            if rsi > 60:
                st.success("🎯 SIGNAL: BUY")
            elif rsi < 40:
                st.error("🎯 SIGNAL: SELL")
            else:
                st.warning("🎯 SIGNAL: WAIT (Market Sideways)")

        # 5. Live Chart Logic
        if 'price_history' not in st.session_state:
            st.session_state.price_history = []
        
        st.session_state.price_history.append(price)
        
        # Chart mein sirf aakhri 20 points rakhna
        if len(st.session_state.price_history) > 20:
            st.session_state.price_history.pop(0)
            
        st.line_chart(st.session_state.price_history)

        # 6. Har 2 second mein page refresh karna
        time.sleep(2)
        st.rerun()

    except Exception as e:
        st.sidebar.error(f"Error: {e}. Check your Keys.")
else:
    # Keys nahi hain toh ye message dikhega
    st.info("👈 Sidebar mein apni **API Key** aur **Access Token** dalo shuru karne ke liye.")
    st.markdown("""
    ### Steps to get started:
    1. **Kite API Key:** Apne Zerodha Developer portal se lein.
    2. **Access Token:** Har subah login karke naya token generate karein.
    3. **Paste & Play:** Dono details sidebar mein daalein aur live trading dashboard shuru!
    """)
