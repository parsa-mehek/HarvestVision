from sklearn.cluster import KMeans


class KMeansLeafCluster:
    def __init__(self, n_clusters=3):
        """
        Initialize K-Means clustering model.
        """
        self.model = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10
        )

    def train(self, X):
        """
        Train K-Means model.
        """
        self.model.fit(X)

    def predict(self, X):
        """
        Predict cluster for new samples.
        """
        return self.model.predict(X)

    def get_cluster_centers(self):
        """
        Return cluster centers.
        """
        return self.model.cluster_centers_

    def get_labels(self):
        """
        Return labels of training data.
        """
        return self.model.labels_

    def get_model(self):
        """
        Return trained K-Means model.
        """
        return self.model