import json
import torch
import joblib
import numpy as np
import pandas as pd

from pytorch_tabnet.tab_model import TabNetClassifier

try:
    from src.ann_model import ANN
except:
    from ann_model import ANN


tabnet = TabNetClassifier()

tabnet.load_model(
    "models/tabnet_model.zip"
)

scaler = joblib.load(
    "models/scaler.pkl"
)

with open(
    "models/model_metadata.json",
    "r"
) as f:

    metadata = json.load(f)

FEATURES = metadata["features"]

embedding_dim = metadata[
    "embedding_dim"
]

ann = ANN(
    embedding_dim
)

ann.load_state_dict(
    torch.load(
        "models/ann_model.pth",
        map_location=torch.device("cpu")
    )
)

ann.eval()


def generate_explanation(
    probability,
    feature_dict
):

    explanation = ""

    if probability >= 0.75:

        explanation += (
            "Patient shows strong indicators "
            "associated with dementia.\n\n"
        )

    elif probability >= 0.50:

        explanation += (
            "Patient shows moderate dementia "
            "risk indicators.\n\n"
        )

    else:

        explanation += (
            "Patient shows relatively low "
            "dementia risk.\n\n"
        )

    if "age" in feature_dict:

        if float(
            feature_dict["age"]
        ) >= 75:

            explanation += (
                f"- Age "
                f"({feature_dict['age']}) "
                f"is a major dementia "
                f"risk factor.\n"
            )

    if "mmse" in feature_dict:

        mmse = float(
            feature_dict["mmse"]
        )

        if mmse < 24:

            explanation += (
                f"- MMSE ({mmse}) "
                f"suggests cognitive "
                f"impairment.\n"
            )

    if "memorycomplaints" in feature_dict:

        if float(
            feature_dict[
                "memorycomplaints"
            ]
        ) == 1:

            explanation += (
                "- Memory complaints "
                "are present.\n"
            )

    if "depression" in feature_dict:

        if float(
            feature_dict[
                "depression"
            ]
        ) == 1:

            explanation += (
                "- Depression may "
                "contribute to "
                "cognitive decline.\n"
            )

    if (
        explanation.strip()
        == ""
    ):

        explanation = (
            "No major clinical "
            "risk factors detected."
        )

    return explanation


def predict(data_dict):

    input_df = pd.DataFrame(
        [data_dict]
    )

    input_df = input_df[
        FEATURES
    ]

    scaled_data = scaler.transform(
        input_df
    )

    latent = tabnet.predict_proba(
        scaled_data
    )

    latent = torch.tensor(
        latent,
        dtype=torch.float32
    )

    probability = ann(
        latent
    ).item()

    confidence = round(
        probability * 100,
        2
    )

    if probability >= 0.75:

        prediction = "Demented"

        risk_level = (
            "VERY HIGH"
        )

    elif probability >= 0.50:

        prediction = (
            "High Risk"
        )

        risk_level = (
            "HIGH"
        )

    elif probability >= 0.30:

        prediction = (
            "Moderate Risk"
        )

        risk_level = (
            "MODERATE"
        )

    else:

        prediction = (
            "Normal"
        )

        risk_level = (
            "LOW"
        )

    explain_matrix, masks = (
        tabnet.explain(
            scaled_data
        )
    )

    importance = np.mean(
        explain_matrix,
        axis=0
    )

    important_features = sorted(
        zip(
            FEATURES,
            importance
        ),
        key=lambda x: x[1],
        reverse=True
    )

    explanation = (
        generate_explanation(
            probability,
            data_dict
        )
    )

    return {

        "prediction":
        prediction,

        "risk_level":
        risk_level,

        "risk_score":
        round(
            probability,
            4
        ),

        "confidence":
        confidence,

        "important_features":
        important_features[:5],

        "explanation":
        explanation
    }