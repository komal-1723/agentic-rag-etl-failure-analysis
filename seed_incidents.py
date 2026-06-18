from db.database import (
    create_table,
    save_incident
)

create_table()

sample_data = [

    (
        "Database timeout",
        "Database",
        "VPN outage",
        "Restart VPN gateway"
    ),

    (
        "Missing Email",
        "Data Quality",
        "Source data issue",
        "Validate source file"
    ),

    (
        "Schema mismatch",
        "Schema",
        "Column renamed",
        "Update ETL mapping"
    ),

    (
        "File not found",
        "File",
        "Source file missing",
        "Verify file path"
    ),

    (
        "Database connection timeout",
        "Database",
        "Network issue",
        "Check connectivity"
    )
]

for incident in sample_data:

    save_incident(
        incident[0],
        incident[1],
        incident[2],
        incident[3]
    )

print(
    "Historical incidents inserted"
)