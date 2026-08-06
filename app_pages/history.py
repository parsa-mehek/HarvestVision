import streamlit as st

from utils.history_manager import HistoryManager


def show_history():
    st.title("Prediction History")

    history = HistoryManager()
    df = history.get_history()

    if df.empty:
        st.info("No prediction history available.")
        return

    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Predictions", len(df))

    with col2:
        if st.button("Clear History"):
            history.clear_history()
            st.success("History cleared successfully.")
            st.rerun()

    st.subheader("Latest Prediction")
    latest = df.iloc[-1]

    st.write(f"**Date:** {latest['Date']}")
    st.write(f"**Predicted Disease:** {latest['Predicted_Disease']}")
    st.write(f"**Model:** {latest['Model']}")
    st.write(f"**Temperature:** {latest['Temperature']}")
    st.write(f"**Humidity:** {latest['Humidity']}")
    st.write(f"**Leaf Color:** {latest['Leaf_Color']}")
    st.write(f"**Leaf Spot:** {latest['Leaf_Spot']}")
    st.write(f"**Leaf Curl:** {latest['Leaf_Curl']}")