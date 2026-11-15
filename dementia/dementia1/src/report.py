import os

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    PageBreak,

    Table,

    TableStyle

)

from reportlab.lib import colors

from reportlab.lib.styles import (

    getSampleStyleSheet,

    ParagraphStyle

)

from reportlab.lib.enums import (
    TA_CENTER
)

from src.history import (
    get_history
)

from src.comparison import (

    compare_assessments,

    get_trend_summary

)


REPORT_FOLDER = (
    "reports/generated_pdfs"
)

os.makedirs(

    REPORT_FOLDER,

    exist_ok=True

)


def get_styles():

    styles = (
        getSampleStyleSheet()
    )

    title_style = ParagraphStyle(

        "ReportTitle",

        parent=styles["Title"],

        alignment=TA_CENTER,

        textColor=colors.HexColor(
            "#2563eb"
        )

    )

    heading_style = ParagraphStyle(

        "Heading",

        parent=styles["Heading2"],

        textColor=colors.HexColor(
            "#2563eb"
        )

    )

    body_style = ParagraphStyle(

        "Body",

        parent=styles["BodyText"],

        leading=20

    )

    return (

        styles,

        title_style,

        heading_style,

        body_style

    )


def create_header(

    elements,

    title_style,

    heading_style,

    report_title

):

    elements.append(

        Paragraph(

            "DementiaAI",

            title_style

        )

    )

    elements.append(

        Paragraph(

            "AI-Based Cognitive Assessment Platform",

            heading_style

        )

    )

    elements.append(
        Spacer(1, 15)
    )

    elements.append(

        Paragraph(

            report_title,

            heading_style

        )

    )

    elements.append(
        Spacer(1, 20)
    )


def create_summary_table(

    data

):

    table = Table(

        data,

        colWidths=[180, 250]

    )

    table.setStyle(

        TableStyle([

            (

                "BACKGROUND",

                (0,0),

                (0,-1),

                colors.HexColor(
                    "#2563eb"
                )

            ),

            (

                "TEXTCOLOR",

                (0,0),

                (0,-1),

                colors.white

            ),

            (

                "GRID",

                (0,0),

                (-1,-1),

                1,

                colors.black

            ),

            (

                "FONTNAME",

                (0,0),

                (0,-1),

                "Helvetica-Bold"

            )

        ])

    )

    return table
def create_latest_report(
    user_id
):

    history = (
        get_history(
            user_id
        )
    )

    if len(history) == 0:

        return None

    latest = history[0]

    file_path = os.path.join(

        REPORT_FOLDER,

        f"latest_{user_id}.pdf"

    )

    doc = SimpleDocTemplate(
        file_path
    )

    (

        styles,

        title_style,

        heading_style,

        body_style

    ) = get_styles()

    elements = []

    create_header(

        elements,

        title_style,

        heading_style,

        "Latest Dementia Assessment Report"

    )

    summary_table = create_summary_table(

        [

            [

                "Prediction",

                str(
                    latest["prediction"]
                )

            ],

            [

                "Risk Level",

                str(
                    latest["risk_level"]
                )

            ],

            [

                "Risk Score",

                str(
                    latest["risk_score"]
                )

            ],

            [

                "Confidence",

                f"{latest['confidence']}%"

            ]

        ]

    )

    elements.append(
        summary_table
    )

    elements.append(
        Spacer(1,20)
    )

    elements.append(

        Paragraph(

            "Clinical Interpretation",

            heading_style

        )

    )

    elements.append(

        Paragraph(

            f"""

            The AI model predicts
            <b>{latest['prediction']}</b>
            with a confidence of
            <b>{latest['confidence']}%</b>.

            The overall dementia
            risk score is
            <b>{latest['risk_score']}</b>.

            This assessment should
            be used as a clinical
            decision-support tool
            and not as a final
            medical diagnosis.

            """,

            body_style

        )

    )

    elements.append(
        Spacer(1,15)
    )

    elements.append(

        Paragraph(

            "Explainable AI Analysis",

            heading_style

        )

    )

    explanation = str(

        latest["explanation"]

    )

    explanation = explanation.replace(

        "-",

        "<br/>•"

    )

    elements.append(

        Paragraph(

            explanation,

            body_style

        )

    )

    elements.append(
        Spacer(1,20)
    )

    elements.append(

        Paragraph(

            "Clinical Recommendation",

            heading_style

        )

    )

    elements.append(

        Paragraph(

            """

            Patients with elevated
            dementia risk should
            undergo periodic
            neurological and
            cognitive evaluation.

            Follow-up assessments
            are recommended to
            monitor progression.

            """,

            body_style

        )

    )

    doc.build(
        elements
    )

    return file_path
def create_history_report(
    user_id
):

    history = (
        get_history(
            user_id
        )
    )

    file_path = os.path.join(

        REPORT_FOLDER,

        f"history_{user_id}.pdf"

    )

    doc = SimpleDocTemplate(
        file_path
    )

    (

        styles,

        title_style,

        heading_style,

        body_style

    ) = get_styles()

    elements = []

    create_header(

        elements,

        title_style,

        heading_style,

        "Assessment History Report"

    )

    history_table = [

        [

            "Date",

            "Prediction",

            "Risk Level",

            "Risk Score"

        ]

    ]

    for item in history:

        history_table.append(

            [

                str(
                    item["date"]
                ),

                str(
                    item["prediction"]
                ),

                str(
                    item["risk_level"]
                ),

                str(
                    item["risk_score"]
                )

            ]

        )

    table = Table(

        history_table,

        colWidths=[
            120,
            120,
            120,
            100
        ]

    )

    table.setStyle(

        TableStyle([

            (

                "BACKGROUND",

                (0,0),

                (-1,0),

                colors.HexColor(
                    "#2563eb"
                )

            ),

            (

                "TEXTCOLOR",

                (0,0),

                (-1,0),

                colors.white

            ),

            (

                "GRID",

                (0,0),

                (-1,-1),

                1,

                colors.black

            ),

            (

                "FONTNAME",

                (0,0),

                (-1,0),

                "Helvetica-Bold"

            )

        ])

    )

    elements.append(
        table
    )

    elements.append(
        Spacer(1,20)
    )

    if len(history) > 0:

        scores = [

            float(
                item["risk_score"]
            )

            for item in history

        ]

        avg_risk = round(

            sum(scores)
            /
            len(scores),

            4

        )

        highest = max(scores)

        lowest = min(scores)

        summary_table = create_summary_table(

            [

                [

                    "Average Risk",

                    str(avg_risk)

                ],

                [

                    "Highest Risk",

                    str(highest)

                ],

                [

                    "Lowest Risk",

                    str(lowest)

                ],

                [

                    "Total Assessments",

                    str(
                        len(history)
                    )

                ]

            ]

        )

        elements.append(

            Paragraph(

                "History Summary",

                heading_style

            )

        )

        elements.append(
            Spacer(1,10)
        )

        elements.append(
            summary_table
        )

    doc.build(
        elements
    )

    return file_path



def create_comparison_report(
    user_id
):

    comparison = (

        compare_assessments(
            user_id
        )

    )

    summary = (

        get_trend_summary(
            user_id
        )

    )

    file_path = os.path.join(

        REPORT_FOLDER,

        f"comparison_{user_id}.pdf"

    )

    doc = SimpleDocTemplate(
        file_path
    )

    (

        styles,

        title_style,

        heading_style,

        body_style

    ) = get_styles()

    elements = []

    create_header(

        elements,

        title_style,

        heading_style,

        "Assessment Comparison Report"

    )

    if comparison["success"]:

        comparison_table = Table(

            [

                [

                    "Metric",

                    "Previous",

                    "Current"

                ],

                [

                    "Prediction",

                    str(
                        comparison[
                            "previous"
                        ][
                            "prediction"
                        ]
                    ),

                    str(
                        comparison[
                            "current"
                        ][
                            "prediction"
                        ]
                    )

                ],

                [

                    "Risk Score",

                    str(
                        comparison[
                            "previous"
                        ][
                            "risk_score"
                        ]
                    ),

                    str(
                        comparison[
                            "current"
                        ][
                            "risk_score"
                        ]
                    )

                ]

            ],

            colWidths=[
                140,
                160,
                160
            ]

        )

        comparison_table.setStyle(

            TableStyle([

                (

                    "BACKGROUND",

                    (0,0),

                    (-1,0),

                    colors.HexColor(
                        "#2563eb"
                    )

                ),

                (

                    "TEXTCOLOR",

                    (0,0),

                    (-1,0),

                    colors.white

                ),

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    1,

                    colors.black

                )

            ])

        )

        elements.append(
            comparison_table
        )

        elements.append(
            Spacer(1,20)
        )

        elements.append(

            Paragraph(

                "Trend Analysis",

                heading_style

            )

        )

        for item in comparison["trend"]:

            elements.append(

                Paragraph(

                    f"• {item}",

                    body_style

                )

            )

        elements.append(
            Spacer(1,20)
        )

    elements.append(

        Paragraph(

            "Overall Summary",

            heading_style

        )

    )

    summary_table = create_summary_table(

        [

            [

                "Average Risk",

                str(
                    summary[
                        "average_risk"
                    ]
                )

            ],

            [

                "Highest Risk",

                str(
                    summary[
                        "highest_risk"
                    ]
                )

            ],

            [

                "Lowest Risk",

                str(
                    summary[
                        "lowest_risk"
                    ]
                )

            ],

            [

                "Total Assessments",

                str(
                    summary[
                        "total_assessments"
                    ]
                )

            ]

        ]

    )

    elements.append(
        summary_table
    )

    elements.append(
        Spacer(1,20)
    )

    elements.append(

        Paragraph(

            """

            This report summarizes
            dementia-risk progression
            across patient assessments.

            Increasing risk scores
            may indicate worsening
            cognitive performance
            and should be reviewed
            by a healthcare professional.

            """,

            body_style

        )

    )

    doc.build(
        elements
    )

    return file_path