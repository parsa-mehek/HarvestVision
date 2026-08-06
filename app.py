import streamlit as st

from app_pages.home import show_home
from app_pages.dashboard import show_dashboard
from app_pages.disease_detection import show_disease_detection
from app_pages.history import show_history

st.set_page_config(page_title="HarvestVision", page_icon="🌿", layout="wide")


def main():
    st.sidebar.title("HarvestVision")

    page = st.sidebar.radio(
        "Navigation",
        ["Home", "Dashboard", "Disease Detection", "History"],
    )

    st.sidebar.markdown("---")

    if page == "Home":
        show_home()
    elif page == "Dashboard":
        show_dashboard()
    elif page == "Disease Detection":
        show_disease_detection()
    elif page == "History":
        show_history()


if __name__ == "__main__":
    main()