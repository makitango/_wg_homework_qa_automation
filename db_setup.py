import sqlite3
import os


def create_db():
    if os.path.exists("ships.db"):
        os.remove("ships.db")

    conn = sqlite3.connect("ships.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
    CREATE TABLE ships (
        ship TEXT PRIMARY KEY,
        weapon TEXT,
        hull TEXT,
        engine TEXT,
        FOREIGN KEY (weapon) REFERENCES weapons(weapon),
        FOREIGN KEY (hull) REFERENCES hulls(hull),
        FOREIGN KEY (engine) REFERENCES engines(engine)
    )
    """)

    cursor.execute("""
    CREATE TABLE weapons (
        weapon TEXT PRIMARY KEY,
        reload_speed INTEGER,
        rotation_speed INTEGER,
        diameter INTEGER,
        power_volley INTEGER,
        count INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE hulls (
        hull TEXT PRIMARY KEY,
        armor INTEGER,
        type INTEGER,
        capacity INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE engines (
        engine TEXT PRIMARY KEY,
        power INTEGER,
        type INTEGER
    )
    """)

    conn.commit()
    conn.close()
    print("DB ships with sub DBs created.")

create_db()