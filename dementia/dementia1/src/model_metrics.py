import json

def get_model_metrics():

    try:

        with open(
            "models/model_metrics.json",
            "r"
        ) as f:

            return json.load(f)

    except:

        return {

            "accuracy": 0,

            "precision": 0,

            "recall": 0,

            "f1_score": 0

        }