import pytest
import sqlite3
import os
from conftest import load_ships_data

original_db_path = "ships.db"

@pytest.fixture(scope="module")
def original_data():
    with sqlite3.connect(original_db_path) as conn:
        return load_ships_data(conn)

@pytest.mark.parametrize("ship_data", load_ships_data(sqlite3.connect(original_db_path)), ids=lambda x: x["name"])
def test_component_comparison(ship_data, randomized_db):
    ship_name = ship_data["name"]
    with sqlite3.connect(randomized_db) as conn:
        cur = conn.cursor()
        cur.execute("SELECT hull, weapon, engine FROM ships WHERE ship = ?", (ship_name,))
        randomized_components = cur.fetchone()
        if randomized_components is None:
            pytest.fail(f"{ship_name} missing in randomized DB")

        randomized_hull, randomized_weapon, randomized_engine = randomized_components

        if randomized_hull != ship_data["hull"]:
            pytest.fail(f"{ship_name}: expected hull {ship_data['hull']}, was {randomized_hull}")
        if randomized_weapon != ship_data["weapon"]:
            pytest.fail(f"{ship_name}: expected weapon {ship_data['weapon']}, was {randomized_weapon}")
        if randomized_engine != ship_data["engine"]:
            pytest.fail(f"{ship_name}: expected engine {ship_data['engine']}, was {randomized_engine}")

        for component, randomized_id in zip(["hulls", "weapons", "engines"], randomized_components):
            original_id = ship_data[component[:-1]]
            cur.execute(f"SELECT * FROM {component} WHERE {component[:-1]} = ?", (original_id,))
            original_row = cur.fetchone()
            cur.execute(f"SELECT * FROM {component} WHERE {component[:-1]} = ?", (randomized_id,))
            randomized_row = cur.fetchone()

            for idx in range(1, len(original_row)):
                param_name = cur.description[idx][0]
                if original_row[idx] != randomized_row[idx]:
                    pytest.fail(f"{ship_name}: {component[:-1]} param '{param_name}' expected {original_row[idx]}, was {randomized_row[idx]}")