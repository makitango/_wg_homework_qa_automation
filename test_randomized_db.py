import sqlite3

def test_randomized_database(randomized_db):
    conn = sqlite3.connect(randomized_db)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM ships")
    assert cur.fetchone()[0] == 200
    conn.close()