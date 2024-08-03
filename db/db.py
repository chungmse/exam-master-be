import sqlite3
from sqlite3 import Connection

DATABASE_URL = "db/exammaster.db"


def get_db() -> Connection:
    connection = sqlite3.connect(DATABASE_URL)
    connection.row_factory = sqlite3.Row
    return connection
