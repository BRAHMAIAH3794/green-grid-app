import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="GreenGrid App", layout="wide")

st.title("⚡ GreenGrid – Energy Usage Forecasting")
st.write("This demo shows live **power usage**, simple **forecast**, and **overload alerts**.")

# 15 Substations
SUBSTATIONS = [f"S{i:02d}" for i in range(1, 16)]
CAPACITY = {sid: np.random.randint(1800, 2600) for sid in SUBSTATIONS}

# Save data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["time", "substation", "load_kW"])
if "alerts" not in st.session_state:
    st.session_state.alerts = []

# Generate data
def generate_data():
    now = datetime.now().strftime("%H:%M:%S")
    sid = np.random.choice(SUBSTATIONS)
    load = int(np.random.normal(2000, 250))
    load = max(200, load)
    return {"time": now, "substation": sid, "load_kW": load}

new_row = generate_data()
st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])]).tail(200)

# Check overload
sid = new_row["substation"]
if new_row["load_kW"] >= 0.9 * CAPACITY[sid]:
    st.session_state.alerts.append(
        f"⚠️ {sid} overload at {new_row['time']} → {new_row['load_kW']} kW (Capacity {CAPACITY[sid]} kW)"
    )

# Tabs
tab1, tab2 = st.tabs(["📊 Live Charts", "🚨 Alerts"])

with tab1:
    st.subheader("Substation Load (kW)")
    choice = st.selectbox("Pick Substation", SUBSTATIONS)
    df = st.session_state.data.query("substation == @choice")
    if not df.empty:
        st.line_chart(df.set_index("time")["load_kW"])
        latest = df["load_kW"].iloc[-1]
        forecast = int(df["load_kW"].tail(5).mean())
        col1, col2, col3 = st.columns(3)
        col1.metric("Capacity", f"{CAPACITY[choice]} kW")
        col2.metric("Current Load", f"{latest} kW")
        col3.metric("Forecast", f"{forecast} kW")

with tab2:
    st.subheader("Recent Alerts")
    if st.session_state.alerts:
        for a in st.session_state.alerts[-10:]:
            st.error(a)
    else:
        st.success("✅ No overloads yet")

st.caption("Demo app – GreenGrid Capstone Project")
