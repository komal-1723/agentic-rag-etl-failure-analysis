import sqlite3


def create_table():

    conn = sqlite3.connect(
        "database/incidents.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        error TEXT,

        category TEXT,

        pipeline_name TEXT,

        status TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


def save_incident(error, category):

    conn = sqlite3.connect(
        "database/incidents.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO incidents(
            error,
            category,
            pipeline_name,
            status
        )
        VALUES (?,?,?,?)
        """,
        (
            error,
            category,
            "Customer_ETL",
            "FAILED"
        )
    )

    conn.commit()
    conn.close()