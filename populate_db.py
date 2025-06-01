import sqlite3
import random
import os

def random_int():
    return random.randint(1, 20)

def populate_db():
    if os.path.exists("ships.db"):
        os.remove("ships.db")

    conn = sqlite3.connect("ships.db")
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE weapons (
        weapon TEXT PRIMARY KEY,
        reload_speed INTEGER,
        rotation_speed INTEGER,
        diameter INTEGER,
        power_volley INTEGER,
        count INTEGER
    );

    CREATE TABLE hulls (
        hull TEXT PRIMARY KEY,
        armor INTEGER,
        type INTEGER,
        capacity INTEGER
    );

    CREATE TABLE engines (
        engine TEXT PRIMARY KEY,
        power INTEGER,
        type INTEGER
    );

    CREATE TABLE ships (
        ship TEXT PRIMARY KEY,
        weapon TEXT,
        hull TEXT,
        engine TEXT,
        FOREIGN KEY(weapon) REFERENCES weapons(weapon),
        FOREIGN KEY(hull) REFERENCES hulls(hull),
        FOREIGN KEY(engine) REFERENCES engines(engine)
    );
    """)

    weapons = []
    for i in range(1, 21):
        name = f"Weapon-{i}"
        data = (name, random_int(), random_int(), random_int(), random_int(), random_int())
        weapons.append(data)
    cursor.executemany("""
        INSERT INTO weapons (weapon, reload_speed, rotation_speed, diameter, power_volley, count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, weapons)

    hulls = []
    for i in range(1, 6):
        name = f"Hull-{i}"
        data = (name, random_int(), random_int(), random_int())
        hulls.append(data)
    cursor.executemany("""
        INSERT INTO hulls (hull, armor, type, capacity)
        VALUES (?, ?, ?, ?)
    """, hulls)

    engines = []
    for i in range(1, 7):
        name = f"Engine-{i}"
        data = (name, random_int(), random_int())
        engines.append(data)
    cursor.executemany("""
        INSERT INTO engines (engine, power, type)
        VALUES (?, ?, ?)
    """, engines)

    ships = []
    for i in range(1, 201):
        name = f"Ship-{i}"
        weapon = random.choice(weapons)[0]
        hull = random.choice(hulls)[0]
        engine = random.choice(engines)[0]
        ships.append((name, weapon, hull, engine))
    cursor.executemany("""
        INSERT INTO ships (ship, weapon, hull, engine)
        VALUES (?, ?, ?, ?)
    """, ships)

    conn.commit()
    conn.close()
    print("DB populated with random values")

if __name__ == "__main__":
    populate_db()
