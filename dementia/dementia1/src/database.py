import sqlite3
import os

DB_FOLDER = "database"

DB_NAME = os.path.join(
    DB_FOLDER,
    "dementia.db"
)


def get_connection():

    os.makedirs(
        DB_FOLDER,
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_NAME
    )

    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # Users Table

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER
        PRIMARY KEY
        AUTOINCREMENT,

        username TEXT
        NOT NULL,

        email TEXT
        UNIQUE
        NOT NULL,

        password TEXT
        NOT NULL,

        created_at
        TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # Assessments Table

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS assessments(

        id INTEGER
        PRIMARY KEY
        AUTOINCREMENT,

        user_id INTEGER,

        prediction TEXT,

        risk_level TEXT,

        risk_score REAL,

        confidence REAL,

        explanation TEXT,

        assessment_date
        TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )

    """)

    # Reports Table

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS reports(

        id INTEGER
        PRIMARY KEY
        AUTOINCREMENT,

        user_id INTEGER,

        report_type TEXT,

        report_path TEXT,

        created_at
        TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )

    """)

    # Migration for old databases

    cursor.execute(
        "PRAGMA table_info(assessments)"
    )

    columns = [

        row[1]

        for row in cursor.fetchall()

    ]

    if "explanation" not in columns:

        cursor.execute("""

        ALTER TABLE assessments

        ADD COLUMN explanation TEXT

        """)

    conn.commit()

    conn.close()


# ======================================
# USER FUNCTIONS
# ======================================

def create_user(

    username,

    email,

    password

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        INSERT INTO users(

            username,
            email,
            password

        )

        VALUES(

            ?,
            ?,
            ?

        )

        """,

        (

            username,
            email,
            password

        )

    )

    conn.commit()

    conn.close()


def get_user_by_email(

    email

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM users

        WHERE email=?

        """,

        (email,)

    )

    user = cursor.fetchone()

    conn.close()

    return user


def get_user_by_id(

    user_id

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM users

        WHERE id=?

        """,

        (user_id,)

    )

    user = cursor.fetchone()

    conn.close()

    return user


# ======================================
# ASSESSMENT FUNCTIONS
# ======================================

def save_assessment(

    user_id,

    prediction,

    risk_level,

    risk_score,

    confidence,

    explanation

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        INSERT INTO assessments(

            user_id,
            prediction,
            risk_level,
            risk_score,
            confidence,
            explanation

        )

        VALUES(

            ?,
            ?,
            ?,
            ?,
            ?,
            ?

        )

        """,

        (

            user_id,
            prediction,
            risk_level,
            risk_score,
            confidence,
            explanation

        )

    )

    conn.commit()

    conn.close()


def get_user_assessments(

    user_id

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM assessments

        WHERE user_id=?

        ORDER BY
        assessment_date DESC

        """,

        (user_id,)

    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_latest_assessment(

    user_id

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM assessments

        WHERE user_id=?

        ORDER BY
        assessment_date DESC

        LIMIT 1

        """,

        (user_id,)

    )

    assessment = cursor.fetchone()

    conn.close()

    return assessment


# ======================================
# REPORT FUNCTIONS
# ======================================

def save_report(

    user_id,

    report_type,

    report_path

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        INSERT INTO reports(

            user_id,
            report_type,
            report_path

        )

        VALUES(

            ?,
            ?,
            ?

        )

        """,

        (

            user_id,
            report_type,
            report_path

        )

    )

    conn.commit()

    conn.close()


def get_user_reports(

    user_id

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM reports

        WHERE user_id=?

        ORDER BY
        created_at DESC

        """,

        (user_id,)

    )

    reports = cursor.fetchall()

    conn.close()

    return reports