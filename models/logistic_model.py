from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score


class LogisticDiseaseModel:
    def __init__(self):
        self.model = OneVsRestClassifier(
            LogisticRegression(
                max_iter=1000,
                random_state=42,
                solver="liblinear",
                C=0.5,
            )
        )

    def train(self, X_train, y_train):
        """
        Train Logistic Regression model.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X):
        """
        Predict disease.
        """
        return self.model.predict(X)

    def predict_proba(self, X):
        """
        Return prediction probabilities.
        """
        return self.model.predict_proba(X)

    def accuracy(self, X_test, y_test):
        """
        Calculate model accuracy.
        """
        prediction = self.model.predict(X_test)
        return accuracy_score(y_test, prediction)

    def get_model(self):
        """
        Return trained model.
        """
        return self.model