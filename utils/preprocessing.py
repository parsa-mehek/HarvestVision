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

NUMERIC_COLUMNS = ["Temperature", "Humidity"]
CATEGORICAL_COLUMNS = ["Leaf_Color", "Leaf_Spot", "Leaf_Curl"]
TARGET_COLUMN = "Disease"


class HarvestPreprocessor:
    """
    Handles preprocessing and encoding for HarvestVision.
    """

    def __init__(self):
        self.numeric_stats = {}
        self.category_levels = {}
        self.feature_columns = []
        self.target_encoder = LabelEncoder()

    def fit(self, df: pd.DataFrame):
        """
        Learn scaling statistics, category levels, and target labels.
        """

        frame = df.copy()

        for col in NUMERIC_COLUMNS:
            numeric_series = pd.to_numeric(frame[col], errors="coerce")
            mean = float(numeric_series.mean())
            std = float(numeric_series.std(ddof=0))

            if pd.isna(mean):
                mean = 0.0
            if pd.isna(std) or std == 0.0:
                std = 1.0

            self.numeric_stats[col] = {"mean": mean, "std": std}

        for col in CATEGORICAL_COLUMNS:
            self.category_levels[col] = sorted(
                frame[col].dropna().astype(str).unique().tolist()
            )

        self.target_encoder.fit(frame[TARGET_COLUMN].astype(str))

        transformed = self._build_feature_frame(frame)
        self.feature_columns = transformed.columns.tolist()

        return self

    def _build_feature_frame(self, df: pd.DataFrame):
        frame = df.copy()
        feature_data = {}

        for col in NUMERIC_COLUMNS:
            stats = self.numeric_stats[col]
            numeric_series = pd.to_numeric(frame[col], errors="coerce")
            numeric_series = numeric_series.fillna(stats["mean"])
            feature_data[col] = (
                (numeric_series - stats["mean"]) / stats["std"]
            ).astype(float)

        for col in CATEGORICAL_COLUMNS:
            values = frame[col].fillna("").astype(str)
            for category in self.category_levels[col]:
                feature_data[f"{col}__{category}"] = (values == category).astype(int)

        return pd.DataFrame(feature_data, index=frame.index)

    def transform(self, df: pd.DataFrame):
        """
        Transform feature columns using fitted feature columns.
        """

        if not self.feature_columns:
            raise ValueError("Preprocessor has not been fitted yet.")

        transformed = self._build_feature_frame(df)
        transformed = transformed.reindex(
            columns=self.feature_columns,
            fill_value=0,
        )

        return transformed

    def encode_target(self, y):
        """
        Encode disease labels into stable numeric classes.
        """

        return self.target_encoder.transform(pd.Series(y).astype(str))

    def decode_target(self, value):
        """
        Convert predicted numeric label back to disease name.
        """

        return self.target_encoder.inverse_transform([int(value)])[0]


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