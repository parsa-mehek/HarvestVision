import streamlit as st
import pandas as pd
import os

from utils.history_manager import HistoryManager


def show_dashboard():
    """
    Display HarvestVision Dashboard.
    """

    st.title("📊 HarvestVision Dashboard")

    st.markdown("---")

    history = HistoryManager()

    total_predictions = history.total_predictions()

    history_df = history.get_history()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Total Predictions",
            value=total_predictions
        )

    with col2:
        if len(history_df) > 0:
            st.metric(
                label="Latest Prediction",
                value=history_df.iloc[-1]["Predicted_Disease"]
            )
        else:
            st.metric(
                label="Latest Prediction",
                value="No Data"
            )

    st.markdown("---")

    st.subheader("Machine Learning Models")

    st.success("✔ Logistic Regression")

    st.success("✔ K-Nearest Neighbors (KNN)")

    st.success("✔ K-Means Clustering")

    st.markdown("---")

    st.subheader("Dataset Information")

    dataset_path = "datasets/crop_disease.csv"

    if os.path.exists(dataset_path):

        df = pd.read_csv(dataset_path)

        st.write("Total Records:", len(df))
        st.write("Total Columns:", len(df.columns))

        st.dataframe(df.head())

    else:

        st.warning("Dataset not found.")

    st.markdown("---")

    st.subheader("Prediction History")

    if len(history_df) > 0:

        st.dataframe(history_df)

    else:

        st.info("No prediction history available.")

    st.markdown("---")

    st.success("HarvestVision Dashboard Loaded Successfully.")