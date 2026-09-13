import sqlite3


def create_database():
    connection = sqlite3.connect("academic.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            task_type TEXT NOT NULL,
            deadline TEXT NOT NULL,
            difficulty INTEGER NOT NULL,
            estimated_hours REAL NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()