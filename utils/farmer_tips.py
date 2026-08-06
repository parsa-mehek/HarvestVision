class FarmerTips:
    """
    Provides farming tips based on the predicted disease.
    """

    def __init__(self):
        self.tips = {

    "Healthy":
        "Maintain regular watering and balanced fertilization.",

    "Rust":
        "Avoid wet leaves and inspect plants regularly.",

    "Early Blight":
        "Rotate crops and keep the field free from infected debris.",

    "Leaf Spot":
        "Maintain proper spacing between plants for better airflow.",

    "Powdery Mildew":
        "Reduce humidity and avoid watering leaves directly."
}

    def get_tip(self, disease):
        """
        Return farming tip for the predicted disease.
        """
        return self.tips.get(
            disease,
            "No farming tips available."
        )

    def get_all_tips(self):
        """
        Return all farming tips.
        """
        return self.tips