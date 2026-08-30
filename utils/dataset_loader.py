import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

from utils.preprocessing import (
    HarvestPreprocessor,
    split_features_target
)


class DatasetLoader:
    def __init__(self, csv_path):
        self.csv_path = Path(csv_path)
        if not self.csv_path.is_absolute():
            self.csv_path = Path(__file__).resolve().parents[1] / self.csv_path
        self.preprocessor = HarvestPreprocessor()

    def load_dataset(self):
        """
        Load dataset from CSV.
        """
        return pd.read_csv(self.csv_path)

    def prepare_data(self):
        """
        Load, preprocess and split dataset.
        """
        df = self.load_dataset()

        self.preprocessor.fit(df)

        # Split features & target
        X, y = split_features_target(df)

        # Encode categorical features
        X = self.preprocessor.transform(X)

        # Encode target
        y = self.preprocessor.encode_target(y)

        return X, y

    def train_test_data(
        self,
        test_size=0.2,
        random_state=42
    ):
        """
        Return train-test split.
        """
        X, y = self.prepare_data()

        return train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=y
        )

    def get_preprocessor(self):
        """
        Return fitted preprocessor.
        """
        return self.preprocessor