import pytest
import shutil
import sqlite3
import tempfile
import random
import os
from db_setup import create_db
from populate_db import populate_db

DB_NAME = "ships.db"

def random_component_value(table, conn):
    cur = conn.cursor()
    pk_col = table[:-1]
    cur.execute(f"SELECT {pk_col} FROM {table}")
    ids = [row[0] for row in cur.fetchall()]
    return random.choice(ids) if ids else None

def random_param_value():
    return random.randint(1, 20)

@pytest.fixture(scope="session")
def randomized_db():
    if not os.path.exists(DB_NAME):
        create_db()
        populate_db()

    temp_db_fd, temp_db_path = tempfile.mkstemp(suffix=".db")
    os.close(temp_db_fd)
    shutil.copyfile(DB_NAME, temp_db_path)

    conn = sqlite3.connect(temp_db_path)
    cur = conn.cursor()

    cur.execute("SELECT ship, hull, weapon, engine FROM ships")
    ships = cur.fetchall()

    for ship_name, hull_id, weapon_id, engine_id in ships:
        if random.choice([True, False]):
            component_to_change = random.choice(["hull", "weapon", "engine"])
            if component_to_change == "hull":
                new_value = random_component_value("hulls", conn)
            elif component_to_change == "weapon":
                new_value = random_component_value("weapons", conn)
            else:
                new_value = random_component_value("engines", conn)
            if new_value is not None:
                cur.execute(f"UPDATE ships SET {component_to_change} = ? WHERE ship = ?", (new_value, ship_name))
        else:
            component_table = random.choice(["hulls", "weapons", "engines"])
            component_id_col = {"hulls": hull_id, "weapons": weapon_id, "engines": engine_id}[component_table]
            if component_id_col is None:
                continue
            cur.execute(f"PRAGMA table_info({component_table})")
            columns = cur.fetchall()
            int_columns = [col[1] for col in columns if col[2] == "INTEGER" and col[1] != component_table[:-1]]
            if not int_columns:
                continue
            param_col = random.choice(int_columns)
            new_param_value = random_param_value()
            cur.execute(f"UPDATE {component_table} SET {param_col} = ? WHERE {component_table[:-1]} = ?", (new_param_value, component_id_col))

    conn.commit()
    yield temp_db_path
    conn.close()
    os.remove(temp_db_path)
