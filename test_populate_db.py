import sqlite3
import os
import pytest
from db_setup import create_db
from populate_db import populate_db

DB_NAME = "ships.db"

@pytest.fixture(scope="module")
def setup_database():
    create_db()
    populate_db()
    yield
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

def get_count(table):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]
    conn.close()
    return count

@pytest.mark.parametrize("table, expected_count", [
    ("weapons", 20),
    ("hulls", 5),
    ("engines", 6),
    ("ships", 200),
])
def test_record_counts(setup_database, table, expected_count):
    assert get_count(table) == expected_count