import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("db/exammaster.db")
cursor = conn.cursor()

# List of table names
tables = [
    "users",
    "subjects",
    "questions",
    "exams",
    "exam_questions",
    "exam_sessions",
    "exam_users",
]

# Disable foreign key checks to avoid issues with deleting data
cursor.execute("PRAGMA foreign_keys = OFF;")

# Delete all data from each table
for table in tables:
    cursor.execute(f"DELETE FROM {table};")
    cursor.execute(
        f'DELETE FROM sqlite_sequence WHERE name="{table}";'
    )  # Reset autoincrement counter

# Re-enable foreign key checks
cursor.execute("PRAGMA foreign_keys = ON;")

# Commit changes and close connection
conn.commit()
conn.close()
