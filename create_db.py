import sqlite3
import os

def create_database():
    if os.path.exists("ships.db"):
        os.remove("ships.db")

    conn = sqlite3.connect("ships.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE ships (
        ship TEXT PRIMARY KEY,
        weapon TEXT,
        hull TEXT,
        engine TEXT
    )""")

    conn.commit()
    conn.close()
    print("DB created")

create_database()