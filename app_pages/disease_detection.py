import pandas as pd
import streamlit as st
from datetime import datetime

from models.knn_model import KNNDiseaseModel
from models.kmeans_model import KMeansLeafCluster
from models.logistic_model import LogisticDiseaseModel
from utils.dataset_loader import DatasetLoader
from utils.farmer_tips import FarmerTips
from utils.fertilizer_recommendation import FertilizerRecommendation
from utils.history_manager import HistoryManager
from utils.image_utils import ImageUtils
from utils.pdf_report import PDFReport
from utils.treatment_recommendation import TreatmentRecommendation


def show_disease_detection():
    st.title("Disease Detection")
    st.caption("Upload a leaf image and predict the disease")

    loader = DatasetLoader("datasets/crop_disease.csv")
    X_train, X_test, y_train, y_test = loader.train_test_data()
    preprocessor = loader.get_preprocessor()

    logistic_model = LogisticDiseaseModel()
    logistic_model.train(X_train, y_train)

    knn_model = KNNDiseaseModel()
    knn_model.train(X_train, y_train)

    kmeans_model = KMeansLeafCluster()
    kmeans_model.train(X_train)

    image_utils = ImageUtils()
    history = HistoryManager()
    fertilizer = FertilizerRecommendation()
    treatment = TreatmentRecommendation()
    tips = FarmerTips()
    pdf_report = PDFReport()

    uploaded_file = st.file_uploader("Upload Leaf Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = image_utils.load_image(uploaded_file)
        if image is not None:
            image = image_utils.resize_image(image)
            image_utils.display_image(image, caption="Uploaded Leaf Image")

    temperature = st.number_input("Temperature", value=25.0)
    humidity = st.number_input("Humidity", value=60.0)
    leaf_color = st.selectbox("Leaf Color", ["Green", "Yellow", "Brown", "Dark Green"])
    leaf_spot = st.selectbox("Leaf Spot", ["Yes", "No"])
    leaf_curl = st.selectbox("Leaf Curl", ["Yes", "No"])
    model_name = st.selectbox("Select Model", ["Logistic Regression", "KNN"])

    if st.button("Predict Disease"):
        if uploaded_file is None:
            st.warning("Please upload a leaf image first.")
            return

        sample = pd.DataFrame(
            [
                {
                    "Temperature": temperature,
                    "Humidity": humidity,
                    "Leaf_Color": leaf_color,
                    "Leaf_Spot": leaf_spot,
                    "Leaf_Curl": leaf_curl,
                }
            ]
        )

        sample = preprocessor.transform(sample)

        if model_name == "Logistic Regression":
            prediction = logistic_model.predict(sample)[0]
        else:
            prediction = knn_model.predict(sample)[0]

        disease = preprocessor.decode_target(prediction)
        cluster = kmeans_model.predict(sample)[0]

        st.success(f"Predicted Disease: {disease}")
        st.info(f"K-Means Cluster: {cluster}")

        st.subheader("Recommendations")
        st.write("**Fertilizer:**", fertilizer.get_recommendation(disease))
        st.write("**Treatment:**", treatment.get_treatment(disease))
        st.write("**Farmer Tip:**", tips.get_tip(disease))

        history.save_prediction(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            temperature=temperature,
            humidity=humidity,
            leaf_color=leaf_color,
            leaf_spot=leaf_spot,
            leaf_curl=leaf_curl,
            predicted_disease=disease,
            model=model_name,
        )

        report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        report_path = pdf_report.generate_report(
            filename=report_name,
            temperature=temperature,
            humidity=humidity,
            leaf_color=leaf_color,
            leaf_spot=leaf_spot,
            leaf_curl=leaf_curl,
            model_name=model_name,
            predicted_disease=disease,
        )

        st.success("Prediction saved successfully.")
        st.success(f"PDF Report: {report_path}")
