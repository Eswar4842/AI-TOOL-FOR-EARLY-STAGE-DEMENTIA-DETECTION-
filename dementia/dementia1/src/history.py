from src.database import (
    get_user_assessments
)


def get_history(
    user_id
):

    rows = (
        get_user_assessments(
            user_id
        )
    )

    history = []

    for row in rows:

        history.append(

            {

                "id":
                row["id"],

                "prediction":
                row["prediction"],

                "risk_level":
                row["risk_level"],

                "risk_score":
                row["risk_score"],

                "confidence":
                row["confidence"],

                "explanation":
                row["explanation"],

                "date":
                row["assessment_date"]

            }

        )

    return history


def get_latest_assessment(
    user_id
):

    history = (
        get_history(
            user_id
        )
    )

    if len(history) == 0:

        return None

    return history[0]


def get_total_assessments(
    user_id
):

    history = (
        get_history(
            user_id
        )
    )

    return len(history)


def get_latest_risk_level(
    user_id
):

    latest = (
        get_latest_assessment(
            user_id
        )
    )

    if latest is None:

        return "N/A"

    return latest[
        "risk_level"
    ]


def get_last_assessment_date(
    user_id
):

    latest = (
        get_latest_assessment(
            user_id
        )
    )

    if latest is None:

        return "N/A"

    return latest[
        "date"
    ]


def get_dashboard_summary(
    user_id
):

    history = (
        get_history(
            user_id
        )
    )

    return {

        "total_assessments":

        len(history),

        "latest_risk":

        get_latest_risk_level(
            user_id
        ),

        "last_date":

        get_last_assessment_date(
            user_id
        ),

        "recent_assessments":

        history[:5]

    }