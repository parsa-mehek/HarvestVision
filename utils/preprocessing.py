"""
utils/preprocessing.py
HarvestVision preprocessing utilities
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder


FEATURE_COLUMNS = [
    "Temperature",
    "Humidity",
    "Leaf_Color",
    "Leaf_Spot",
    "Leaf_Curl",
]

TARGET_COLUMN = "Disease"


class HarvestPreprocessor:
    """
    Handles preprocessing and encoding for HarvestVision.
    """

    def __init__(self):
        self.encoders = {}

    def fit(self, df: pd.DataFrame):
        """
        Fit encoders for feature columns only.
        """

        categorical = [
            "Leaf_Color",
            "Leaf_Spot",
            "Leaf_Curl"
        ]

        for col in categorical:
            encoder = LabelEncoder()
            df[col] = encoder.fit_transform(df[col].astype(str))
            self.encoders[col] = encoder

        return df

    def transform(self, df: pd.DataFrame):
        """
        Transform feature columns using fitted encoders.
        """

        categorical = [
            "Leaf_Color",
            "Leaf_Spot",
            "Leaf_Curl"
        ]

        for col in categorical:

            if col not in self.encoders:
                raise ValueError(f"Encoder for '{col}' is not fitted.")

            encoder = self.encoders[col]

            values = []

            for value in df[col].astype(str):

                if value not in encoder.classes_:
                    value = encoder.classes_[0]

                values.append(value)

            df[col] = encoder.transform(values)

        return df

    def encode_target(self, y):
     
        y = pd.Series(y).astype(str)

        encoder = LabelEncoder()
        encoded = encoder.fit_transform(y)

        self.encoders["Disease"] = encoder

        return encoded

    def decode_target(self, value):
        """
        Convert predicted numeric label back to disease name.
        """

        return self.encoders["Disease"].inverse_transform([int(value)])[0]


def load_dataset(csv_path: str):
    """
    Load HarvestVision dataset.
    """

    return pd.read_csv(csv_path)


def split_features_target(df: pd.DataFrame):
    """
    Split dataset into X and y.
    """

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    return X, y