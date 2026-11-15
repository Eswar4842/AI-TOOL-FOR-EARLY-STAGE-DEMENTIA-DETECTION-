from src.history import (
    get_history
)


def compare_assessments(
    user_id
):

    history = (
        get_history(
            user_id
        )
    )

    if len(history) < 2:

        return {

            "success": False,

            "message":
            "At least two assessments required"

        }

    current = history[0]

    previous = history[1]

    comparison = {

        "risk_score": {

            "previous":
            previous["risk_score"],

            "current":
            current["risk_score"],

            "change":
            round(

                current["risk_score"]
                -
                previous["risk_score"],

                4

            )
        },

        "confidence": {

            "previous":
            previous["confidence"],

            "current":
            current["confidence"],

            "change":
            round(

                current["confidence"]
                -
                previous["confidence"],

                2

            )
        }

    }

    trend = []

    if (
        current["risk_score"]
        >
        previous["risk_score"]
    ):

        trend.append(

            "Overall dementia risk has increased."

        )

    elif (
        current["risk_score"]
        <
        previous["risk_score"]
    ):

        trend.append(

            "Overall dementia risk has decreased."

        )

    else:

        trend.append(

            "Risk level remains unchanged."

        )

    if (
        current["confidence"]
        >
        previous["confidence"]
    ):

        trend.append(

            "Prediction confidence increased."

        )

    elif (
        current["confidence"]
        <
        previous["confidence"]
    ):

        trend.append(

            "Prediction confidence decreased."

        )

    return {

        "success": True,

        "previous":
        previous,

        "current":
        current,

        "comparison":
        comparison,

        "trend":
        trend

    }


def get_risk_progression(
    user_id
):

    history = (
        get_history(
            user_id
        )
    )

    progression = []

    for item in history:

        progression.append(

            {

                "date":
                item["date"],

                "risk_score":
                item["risk_score"]

            }

        )

    progression.reverse()

    return progression


def get_prediction_progression(
    user_id
):

    history = (
        get_history(
            user_id
        )
    )

    progression = []

    for item in history:

        progression.append(

            {

                "date":
                item["date"],

                "prediction":
                item["prediction"]

            }

        )

    progression.reverse()

    return progression


def get_trend_summary(
    user_id
):

    history = (
        get_history(
            user_id
        )
    )

    if len(history) == 0:

        return {

            "message":
            "No assessments found"
        }

    risk_scores = [

        item["risk_score"]

        for item in history

    ]

    avg_risk = round(

        sum(risk_scores)
        /
        len(risk_scores),

        4

    )

    highest_risk = max(
        risk_scores
    )

    lowest_risk = min(
        risk_scores
    )

    return {

        "average_risk":
        avg_risk,

        "highest_risk":
        highest_risk,

        "lowest_risk":
        lowest_risk,

        "total_assessments":
        len(history)

    }