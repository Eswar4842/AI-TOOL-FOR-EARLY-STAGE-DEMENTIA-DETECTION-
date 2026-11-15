
import os
import sys
import json
import torch
import subprocess
import numpy as np
from imblearn.over_sampling import SMOTE

from pytorch_tabnet.tab_model import TabNetClassifier

from sklearn.model_selection import train_test_split

from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score,

    classification_report

)

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

try:

    from src.preprocess import (
        preprocess_data
    )

    from src.ann_model import (
        ANN
    )

except ModuleNotFoundError:

    from preprocess import (
        preprocess_data
    )

    from ann_model import (
        ANN
    )

os.makedirs(
    "models",
    exist_ok=True
)

# ---------------------------------
# Feature Selection
# ---------------------------------

if not os.path.exists(
    "models/top_features.json"
):

    print(
        "\nRunning Feature Selection..."
    )

    subprocess.run(

        [

            sys.executable,

            "src/feature_selection.py"

        ],

        check=True

    )

# ---------------------------------
# Load Data
# ---------------------------------

X, y, feature_names = preprocess_data(

    "data/alzheimers_disease_data.csv"

)

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42,

    stratify=y

)
smote = SMOTE(
    random_state=42
)

X_train, y_train = smote.fit_resample(
    X_train,
    y_train
)

print(
    "\nDataset Loaded"
)

print(
    f"Training Samples : {len(X_train)}"
)

print(
    f"Testing Samples  : {len(X_test)}"
)

# ---------------------------------
# Train TabNet
# ---------------------------------

print(
    "\nTraining TabNet..."
)

tabnet = TabNetClassifier(

    n_d=64,

    n_a=64,

    n_steps=5,

    gamma=1.5,

    lambda_sparse=1e-4

)

tabnet.fit(

    X_train,

    y_train,

    eval_set=[

        (

            X_test,

            y_test

        )

    ],

    max_epochs=150,

    patience=30

)

tabnet.save_model(
    "models/tabnet_model"
)

print(
    "TabNet Saved"
)

# ---------------------------------
# Latent Features
# ---------------------------------

X_train_latent = tabnet.predict_proba(
    X_train
)

X_test_latent = tabnet.predict_proba(
    X_test
)

X_train_latent = torch.tensor(

    X_train_latent,

    dtype=torch.float32

)

X_test_latent = torch.tensor(

    X_test_latent,

    dtype=torch.float32

)

y_train_tensor = torch.tensor(

    np.array(y_train),

    dtype=torch.float32

).reshape(-1, 1)

# ---------------------------------
# Train ANN
# ---------------------------------

print(
    "\nTraining ANN..."
)

ann = ANN(
    X_train_latent.shape[1]
)

criterion = torch.nn.BCELoss()

optimizer = torch.optim.Adam(

    ann.parameters(),

    lr=0.001

)
scheduler = torch.optim.lr_scheduler.StepLR(

    optimizer,

    step_size=50,

    gamma=0.5

)

for epoch in range(300):

    optimizer.zero_grad()

    output = ann(
        X_train_latent
    )

    loss = criterion(

        output,

        y_train_tensor

    )

    loss.backward()

    optimizer.step()
    scheduler.step()

    if epoch % 10 == 0:

        print(

            f"Epoch {epoch}"

            f" | Loss: {loss.item():.4f}"

        )

torch.save(

    ann.state_dict(),

    "models/ann_model.pth"

)

print(
    "\nANN Saved"
)

# ---------------------------------
# Evaluate Model
# ---------------------------------

print(
    "\nEvaluating Model..."
)

with torch.no_grad():

    predictions = ann(
        X_test_latent
    )

predictions = (
    predictions.numpy() > 0.4
).astype(int)

accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions
)

recall = recall_score(
    y_test,
    predictions
)

f1 = f1_score(
    y_test,
    predictions
)

print("\nModel Performance")

print(
    f"Accuracy : {accuracy*100:.2f}%"
)

print(
    f"Precision: {precision*100:.2f}%"
)

print(
    f"Recall   : {recall*100:.2f}%"
)

print(
    f"F1 Score : {f1*100:.2f}%"
)

print(
    "\nClassification Report\n"
)

print(

    classification_report(

        y_test,

        predictions

    )

)

# ---------------------------------
# Save Metrics
# ---------------------------------

metrics = {

    "accuracy":

    round(
        accuracy * 100,
        2
    ),

    "precision":

    round(
        precision * 100,
        2
    ),

    "recall":

    round(
        recall * 100,
        2
    ),

    "f1_score":

    round(
        f1 * 100,
        2
    )

}

with open(

    "models/model_metrics.json",

    "w"

) as f:

    json.dump(

        metrics,

        f,

        indent=4

    )

print(
    "\nMetrics Saved"
)

# ---------------------------------
# Save Metadata
# ---------------------------------

feature_importance = {}

for feature, importance in zip(

    feature_names,

    tabnet.feature_importances_

):

    feature_importance[
        feature
    ] = float(
        importance
    )

metadata = {

    "embedding_dim":

    int(
        X_train_latent.shape[1]
    ),

    "num_features":

    len(
        feature_names
    ),

    "features":

    feature_names,

    "feature_importance":

    feature_importance

}

with open(

    "models/model_metadata.json",

    "w"

) as f:

    json.dump(

        metadata,

        f,

        indent=4

    )

print(
    "\nMetadata Saved"
)

print(
    "\nTraining Completed Successfully"
)
