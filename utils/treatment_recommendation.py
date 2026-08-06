class TreatmentRecommendation:
    """
    Provides treatment recommendations
    based on predicted disease.
    """

    def __init__(self):
        self.treatments = {

    "Healthy":
        "No treatment required. Continue regular monitoring.",

    "Rust":
        "Apply a recommended fungicide and remove infected leaves.",

    "Early Blight":
        "Spray copper-based fungicide and remove infected leaves.",

    "Leaf Spot":
        "Prune infected leaves and apply fungicide.",

    "Powdery Mildew":
        "Use sulfur or neem oil spray and improve air circulation."
}

    def get_treatment(self, disease):
        """
        Return treatment recommendation.
        """

        return self.treatments.get(
            disease,
            "No treatment recommendation available."
        )

    def get_all_treatments(self):
        """
        Return all treatment recommendations.
        """

        return self.treatments