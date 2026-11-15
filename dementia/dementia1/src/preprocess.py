import os
import json
import joblib
import pandas as pd

from sklearn.preprocessing import MinMaxScaler


def preprocess_data(path):

    df = pd.read_csv(path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    if "diagnosis" not in df.columns:
        raise KeyError(
            "Diagnosis column not found"
        )

    if not os.path.exists(
        "models/top_features.json"
    ):
        raise FileNotFoundError(
            "Run feature_selection.py first"
        )

    with open(
        "models/top_features.json",
        "r"
    ) as f:

        features = json.load(f)

    y = df["diagnosis"]

    X = df[features].copy()

    X = X.fillna(
        X.mean(numeric_only=True)
    )

    scaler = MinMaxScaler()

    X_scaled = scaler.fit_transform(X)

    os.makedirs(
        "models",
        exist_ok=True
    )

    joblib.dump(
        scaler,
        "models/scaler.pkl"
    )

    return (
        X_scaled,
        y,
        features
    )