# demo_security_test.py
import sqlite3

def find_user(email: str):
    connection = sqlite3.connect("demo.db")
    query = f"SELECT * FROM users WHERE email = '{email}'"
    return connection.execute(query).fetchall()