class FertilizerRecommendation:
    """
    Provides fertilizer recommendations
    based on predicted disease.
    """

    def __init__(self):
       self.recommendations = {

    "Healthy":
        "Apply balanced NPK (10-10-10) and organic compost regularly.",

    "Rust":
        "Use potassium-rich fertilizer and avoid excessive nitrogen.",

    "Early Blight":
        "Apply nitrogen-rich fertilizer and maintain proper irrigation.",

    "Leaf Spot":
        "Use balanced NPK fertilizer and remove infected leaves.",

    "Powdery Mildew":
        "Apply phosphorus-rich fertilizer and avoid overwatering."
}

    def get_recommendation(self, disease):
        """
        Return fertilizer recommendation.
        """

        return self.recommendations.get(
            disease,
            "No fertilizer recommendation available."
        )

    def get_all_recommendations(self):
        """
        Return all recommendations.
        """

        return self.recommendations