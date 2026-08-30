import os
import pandas as pd
from pathlib import Path


class HistoryManager:
    def __init__(self, history_file="history.csv"):
        history_path = Path(history_file)
        if not history_path.is_absolute():
            history_path = Path(__file__).resolve().parents[1] / history_path

        self.history_file = str(history_path)

        if not os.path.exists(self.history_file):
            columns = [
                "Date",
                "Temperature",
                "Humidity",
                "Leaf_Color",
                "Leaf_Spot",
                "Leaf_Curl",
                "Predicted_Disease",
                "Model"
            ]

            pd.DataFrame(columns=columns).to_csv(
                self.history_file,
                index=False
            )

    def save_prediction(
        self,
        date,
        temperature,
        humidity,
        leaf_color,
        leaf_spot,
        leaf_curl,
        predicted_disease,
        model
    ):
        """
        Save prediction history.
        """

        new_data = {
            "Date": date,
            "Temperature": temperature,
            "Humidity": humidity,
            "Leaf_Color": leaf_color,
            "Leaf_Spot": leaf_spot,
            "Leaf_Curl": leaf_curl,
            "Predicted_Disease": predicted_disease,
            "Model": model
        }

        df = pd.read_csv(self.history_file)

        df = pd.concat(
            [df, pd.DataFrame([new_data])],
            ignore_index=True
        )

        df.to_csv(self.history_file, index=False)

    def get_history(self):
        """
        Return all prediction history.
        """

        return pd.read_csv(self.history_file)

    def clear_history(self):
        """
        Delete all history.
        """

        columns = [
            "Date",
            "Temperature",
            "Humidity",
            "Leaf_Color",
            "Leaf_Spot",
            "Leaf_Curl",
            "Predicted_Disease",
            "Model"
        ]

        pd.DataFrame(columns=columns).to_csv(
            self.history_file,
            index=False
        )

    def total_predictions(self):
        """
        Return total prediction count.
        """

        df = pd.read_csv(self.history_file)

        return len(df)