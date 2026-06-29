import sqlite3

DB_PATH = "database/incidents.db"


def create_table():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        error TEXT NOT NULL,

        category TEXT NOT NULL,

        cause TEXT,

        fix TEXT,

        pipeline_name TEXT,

        status TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


def save_incident(
    error,
    category,
    cause="Unknown",
    fix="Pending Investigation"
):
    """
    Saves an ETL incident.

    Parameters
    ----------
    error : str
        Error message.

    category : str
        Error category.

    cause : str, optional
        Root cause.
        Defaults to "Unknown".

    fix : str, optional
        Recommended fix.
        Defaults to "Pending Investigation".
    """

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO incidents(

            error,
            category,
            cause,
            fix,
            pipeline_name,
            status

        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            error,
            category,
            cause,
            fix,
            "Customer_ETL",
            "FAILED"
        )
    )

    conn.commit()
    conn.close()


def fetch_all_incidents():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM incidents
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def fetch_incident_by_id(incident_id):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM incidents
        WHERE id = ?
        """,
        (incident_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return row