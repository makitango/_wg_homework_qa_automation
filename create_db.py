import sqlite3
import os

def create_db():
    print(os.path.exists("imaginary_db.db"))

create_db()