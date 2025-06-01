import sqlite3
import pytest
from populate_db import populate_db
from db_setup import create_db

def get_ship_components(conn):
    cur = conn.cursor()
    cur.execute("SELECT ship, weapon, hull, engine FROM ships")
    return {row[0]: (row[1], row[2], row[3]) for row in cur.fetchall()}

def get_component_params(conn, table, component_id):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    columns = [col[1] for col in cur.fetchall() if col[1] != table[:-1]]
    cur.execute(f"SELECT {', '.join(columns)} FROM {table} WHERE {table[:-1]} = ?", (component_id,))
    row = cur.fetchone()
    return dict(zip(columns, row)) if row else {}

def compare_components(ship, comp_type, orig_id, rand_id, orig_conn, rand_conn, failures):
    if orig_id != rand_id:
        failures.append(f"{ship}: expected {comp_type} {orig_id}, was {rand_id}")
        return
    orig_params = get_component_params(orig_conn, comp_type + "s", orig_id)
    rand_params = get_component_params(rand_conn, comp_type + "s", rand_id)
    for param in orig_params:
        if orig_params[param] != rand_params.get(param):
            failures.append(f"{ship}: {comp_type} param '{param}' expected {orig_params[param]}, was {rand_params.get(param)}")

def test_compare_original_and_randomized_db(randomized_db):
    original_path = "ships.db"
    orig_conn = sqlite3.connect(original_path)
    rand_conn = sqlite3.connect(randomized_db)
    orig_data = get_ship_components(orig_conn)
    rand_data = get_ship_components(rand_conn)
    failures = []
    for ship in orig_data:
        orig_weapon, orig_hull, orig_engine = orig_data[ship]
        rand_weapon, rand_hull, rand_engine = rand_data[ship]
        compare_components(ship, "weapon", orig_weapon, rand_weapon, orig_conn, rand_conn, failures)
        compare_components(ship, "hull", orig_hull, rand_hull, orig_conn, rand_conn, failures)
        compare_components(ship, "engine", orig_engine, rand_engine, orig_conn, rand_conn, failures)
    orig_conn.close()
    rand_conn.close()
    if failures:
        pytest.fail("\n" + "\n".join(failures))