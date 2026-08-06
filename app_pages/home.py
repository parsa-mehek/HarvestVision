import streamlit as st


def show_home():
    """
    Display the Home Page.
    """

    st.title("HarvestVision")
    st.subheader("Smart Crop Disease Detection System")

    st.markdown("---")

    st.write("""
    Welcome to **HarvestVision**.

    HarvestVision is a Machine Learning based crop disease prediction
    """)

    st.markdown("---")

    st.header("Project Features")

    st.success("✔ Disease Prediction")

    st.success("✔ Logistic Regression")

    st.success("✔ KNN Classification")

    st.success("✔ K-Means Clustering")

    st.success("✔ Fertilizer Recommendation")

    st.success("✔ Treatment Recommendation")

    st.success("✔ Farmer Tips")

    st.success("✔ Prediction History")

    st.success("✔ PDF Report")

    st.markdown("---")

    st.info(
        "Use the navigation menu on the left to explore different pages."
    )