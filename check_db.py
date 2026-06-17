import sqlite3

conn = sqlite3.connect(
    "database/incidents.db"
)

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM incidents"
)

rows = cursor.fetchall()

print("\nINCIDENTS TABLE\n")

for row in rows:
    print(
        f"ID={row[0]}"
        f" | ERROR={row[1]}"
        f" | CATEGORY={row[2]}"
        f" | PIPELINE={row[3]}"
        f" | STATUS={row[4]}"
        f" | CREATED_AT={row[5]}"
    )

   

conn.close()