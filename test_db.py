import os
from db_setup import create_db

def test_db_file_created():
    if os.path.exists("ships.db"):
        os.remove("ships.db")
    create_db()
    assert os.path.exists("ships.db")