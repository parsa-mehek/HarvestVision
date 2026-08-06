from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


class KNNDiseaseModel:
    def __init__(self, n_neighbors=5):
        """
        Initialize KNN model.
        """
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors)

    def train(self, X_train, y_train):
        """
        Train KNN model.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X):
        """
        Predict disease.
        """
        return self.model.predict(X)

    def accuracy(self, X_test, y_test):
        """
        Calculate model accuracy.
        """
        prediction = self.model.predict(X_test)
        return accuracy_score(y_test, prediction)

    def get_model(self):
        """
        Return trained KNN model.
        """
        return self.model