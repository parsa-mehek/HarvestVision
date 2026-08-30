import pandas as pd
from random import Random


class KMeansLeafCluster:
    def __init__(self, n_clusters=3, max_iter=100, random_state=42):
        """
        Initialize K-Means clustering model.
        """

        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids = None
        self.labels_ = None
        self.feature_columns = []

    def _prepare_frame(self, X):
        frame = X.copy() if isinstance(X, pd.DataFrame) else pd.DataFrame(X)

        if self.feature_columns:
            frame = frame.reindex(columns=self.feature_columns, fill_value=0)
        else:
            self.feature_columns = frame.columns.tolist()

        return frame.astype(float)

    @staticmethod
    def _squared_distance(row, centroid):
        return sum((row[column] - centroid[column]) ** 2 for column in row.index)

    def train(self, X):
        """
        Train K-Means model.
        """

        frame = self._prepare_frame(X).reset_index(drop=True)

        if len(frame) < self.n_clusters:
            raise ValueError("K-Means requires at least as many rows as clusters.")

        random = Random(self.random_state)
        initial_indices = list(range(len(frame)))
        random.shuffle(initial_indices)
        centroid_rows = frame.iloc[initial_indices[: self.n_clusters]].copy().reset_index(drop=True)

        labels = [0] * len(frame)

        for _ in range(self.max_iter):
            changed = False

            for index, row in frame.iterrows():
                distances = [
                    self._squared_distance(row, centroid_rows.iloc[cluster_index])
                    for cluster_index in range(self.n_clusters)
                ]
                label = distances.index(min(distances))

                if labels[index] != label:
                    changed = True

                labels[index] = label

            new_centroids = []
            for cluster_index in range(self.n_clusters):
                cluster_points = frame[[label == cluster_index for label in labels]]

                if cluster_points.empty:
                    new_centroids.append(centroid_rows.iloc[cluster_index])
                else:
                    new_centroids.append(cluster_points.mean(numeric_only=True))

            new_centroid_rows = pd.DataFrame(new_centroids).reset_index(drop=True)

            if not changed or new_centroid_rows.equals(centroid_rows):
                centroid_rows = new_centroid_rows
                break

            centroid_rows = new_centroid_rows

        self.centroids = centroid_rows
        self.labels_ = labels

        return self

    def predict(self, X):
        """
        Predict cluster for new samples.
        """

        if self.centroids is None:
            raise ValueError("K-Means model has not been trained yet.")

        frame = self._prepare_frame(X).reset_index(drop=True)
        predictions = []

        for _, row in frame.iterrows():
            distances = [
                self._squared_distance(row, self.centroids.iloc[cluster_index])
                for cluster_index in range(self.n_clusters)
            ]
            predictions.append(distances.index(min(distances)))

        return predictions

    def get_cluster_centers(self):
        """
        Return cluster centers.
        """

        return None if self.centroids is None else self.centroids.copy()

    def get_labels(self):
        """
        Return labels of training data.
        """

        return self.labels_

    def get_model(self):
        """
        Return trained K-Means model.
        """

        return self