from flask import (

    Flask,

    render_template,

    request,

    redirect,

    url_for,

    session,

    flash,

    send_file

)

import os
from src.model_metrics import (
    get_model_metrics
)
from src.database import (
    initialize_database,
    save_assessment
)

from src.auth import (

    register_user,

    login_user,

    get_current_user

)

from src.history import (

    get_history,

    get_dashboard_summary,

    get_latest_risk_level,

    get_last_assessment_date,

    get_total_assessments

)

from src.comparison import (

    compare_assessments,

    get_trend_summary

)

from src.report import (

    create_latest_report,

    create_history_report,

    create_comparison_report

)

from src.predict import predict


app = Flask(__name__)

app.secret_key = (
    "dementia_ai_secret_key"
)

initialize_database()


def login_required():

    return (
        "user_id" in session
    )


@app.route("/")
def landing():

    if "user_id" in session:

        return redirect(
            url_for(
                "dashboard"
            )
        )

    return render_template(
        "landing.html"
    )


@app.route(
    "/signup",
    methods=[
        "GET",
        "POST"
    ]
)
def signup():

    if request.method == "POST":

        username = request.form[
            "username"
        ]

        email = request.form[
            "email"
        ]

        password = request.form[
            "password"
        ]

        result = register_user(

            username,

            email,

            password

        )

        if result["success"]:

            flash(
                "Account created successfully"
            )

            return redirect(
                url_for(
                    "login"
                )
            )

        flash(
            result["message"]
        )

    return render_template(
        "signup.html"
    )


@app.route(
    "/login",
    methods=[
        "GET",
        "POST"
    ]
)
def login():

    if request.method == "POST":

        email = request.form[
            "email"
        ]

        password = request.form[
            "password"
        ]

        result = login_user(

            email,

            password

        )

        if result["success"]:

            session[
                "user_id"
            ] = result[
                "user_id"
            ]

            session[
                "username"
            ] = result[
                "username"
            ]

            return redirect(
                url_for(
                    "dashboard"
                )
            )

        flash(
            result["message"]
        )

    return render_template(
        "login.html"
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for(
            "landing"
        )
    )


@app.route("/dashboard")
def dashboard():

    if not login_required():

        return redirect(
            url_for("login")
        )

    summary = (
        get_dashboard_summary(
            session["user_id"]
        )
    )

    metrics = (
        get_model_metrics()
    )

    return render_template(

        "dashboard.html",

        summary=summary,

        metrics=metrics

    )


@app.route(
    "/assessment",
    methods=[
        "GET",
        "POST"
    ]
)
def assessment():

    if not login_required():

        return redirect(
            url_for(
                "login"
            )
        )

    result = None

    if request.method == "POST":

        try:

            patient_data = {

                "adl":
                float(
                    request.form["adl"]
                ),

                "memorycomplaints":
                float(
                    request.form[
                        "memorycomplaints"
                    ]
                ),

                "functionalassessment":
                float(
                    request.form[
                        "functionalassessment"
                    ]
                ),

                "sleepquality":
                float(
                    request.form[
                        "sleepquality"
                    ]
                ),

                "mmse":
                float(
                    request.form[
                        "mmse"
                    ]
                ),

                "bmi":
                float(
                    request.form[
                        "bmi"
                    ]
                ),

                "cardiovasculardisease":
                float(
                    request.form[
                        "cardiovasculardisease"
                    ]
                ),

                "depression":
                float(
                    request.form[
                        "depression"
                    ]
                ),

                "age":
                float(
                    request.form[
                        "age"
                    ]
                ),

                "difficultycompletingtasks":
                float(
                    request.form[
                        "difficultycompletingtasks"
                    ]
                )

            }

            result = predict(
                patient_data
            )

            save_assessment(

                session[
                    "user_id"
                ],

                result[
                    "prediction"
                ],

                result[
                    "risk_level"
                ],

                result[
                    "risk_score"
                ],

                result[
                    "confidence"
                ],

                result[
                    "explanation"
                ]

            )

        except Exception as e:

            result = {

                "prediction":
                "Error",

                "risk_level":
                "N/A",

                "risk_score":
                0,

                "confidence":
                0,

                "explanation":
                str(e)

            }

    return render_template(

        "assessment.html",

        result=result

    )


@app.route("/history")
def history():

    if not login_required():

        return redirect(
            url_for(
                "login"
            )
        )

    history_data = (
        get_history(
            session[
                "user_id"
            ]
        )
    )

    return render_template(

        "history.html",

        history=history_data

    )


@app.route("/comparison")
def comparison():

    if not login_required():

        return redirect(
            url_for(
                "login"
            )
        )

    comparison_data = (

        compare_assessments(

            session[
                "user_id"
            ]

        )

    )

    trend_summary = (

        get_trend_summary(

            session[
                "user_id"
            ]

        )

    )

    return render_template(

        "comparison.html",

        comparison=
        comparison_data,

        summary=
        trend_summary

    )


@app.route("/profile")
def profile():

    if not login_required():

        return redirect(
            url_for(
                "login"
            )
        )

    user = (
        get_current_user(
            session[
                "user_id"
            ]
        )
    )

    return render_template(

        "profile.html",

        user=user,

        total_assessments=
        get_total_assessments(
            session[
                "user_id"
            ]
        ),

        latest_risk=
        get_latest_risk_level(
            session[
                "user_id"
            ]
        ),

        last_assessment=
        get_last_assessment_date(
            session[
                "user_id"
            ]
        )

    )


@app.route("/settings")
def settings():

    if not login_required():

        return redirect(
            url_for(
                "login"
            )
        )

    user = (
        get_current_user(
            session[
                "user_id"
            ]
        )
    )

    return render_template(

        "settings.html",

        user=user

    )


@app.route("/reports")
def reports():

    if not login_required():

        return redirect(
            url_for(
                "login"
            )
        )

    history = (
        get_history(
            session[
                "user_id"
            ]
        )
    )

    return render_template(

        "reports.html",

        reports_count=
        len(history),

        latest_download=
        "Not Downloaded"

    )


@app.route(
    "/download/latest"
)
def download_latest():

    path = (
        create_latest_report(
            session[
                "user_id"
            ]
        )
    )

    return send_file(

        path,

        as_attachment=True

    )


@app.route(
    "/download/history"
)
def download_history():

    path = (
        create_history_report(
            session[
                "user_id"
            ]
        )
    )

    return send_file(

        path,

        as_attachment=True

    )


@app.route(
    "/download/comparison"
)
def download_comparison():

    path = (
        create_comparison_report(
            session[
                "user_id"
            ]
        )
    )

    return send_file(

        path,

        as_attachment=True

    )


if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )