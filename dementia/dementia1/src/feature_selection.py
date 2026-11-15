import os
import json
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from pytorch_tabnet.tab_model import TabNetClassifier


os.makedirs(
    "models",
    exist_ok=True
)

print(
    "\nStarting TabNet Feature Selection..."
)

df = pd.read_csv(
    "data/alzheimers_disease_data.csv"
)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)

if "diagnosis" not in df.columns:
    raise KeyError(
        "Diagnosis column not found"
    )

y = df["diagnosis"]

drop_columns = [
    "diagnosis",
    "patientid",
    "doctorincharge"
]

X = df.drop(
    columns=drop_columns,
    errors="ignore"
)

X = X.fillna(
    X.mean(numeric_only=True)
)

scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(X)

tabnet = TabNetClassifier(
    n_d=16,
    n_a=16,
    n_steps=5,
    gamma=1.5,
    lambda_sparse=1e-4
)

tabnet.fit(
    X_scaled,
    y,
    max_epochs=50
)

importance_df = pd.DataFrame(
    {
        "feature": X.columns,
        "importance":
        tabnet.feature_importances_
    }
)

importance_df = (
    importance_df
    .sort_values(
        by="importance",
        ascending=False
    )
)

top_features = (
    importance_df
    .head(10)["feature"]
    .tolist()
)

print(
    "\nTop 10 Features Selected:\n"
)

for idx, feature in enumerate(
    top_features,
    start=1
):

    print(
        f"{idx}. {feature}"
    )

with open(
    "models/top_features.json",
    "w"
) as f:

    json.dump(
        top_features,
        f,
        indent=4
    )

print(
    "\nSaved:"
)

print(
    "models/top_features.json"
)

print(
    "\nFeature Selection Completed Successfully"
)