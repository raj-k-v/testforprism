# demo_bad_pr.py — intentionally flawed, for testing the review bot

import sqlite3
import os

API_KEY = "sk-live-51H8xJ2eZvKYlo2C9gQ7t3mF4nR8pL0w"  # hardcoded secret — security

def get_user(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # string-formatted SQL — classic SQL injection
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

def divide_scores(scores, total):
    # no guard against total == 0 — runtime bug
    return [s / total for s in scores]

def load_config(path):
    f = open(path)          # file handle never closed — resource leak
    data = f.read()
    return data

def find_duplicates(items):
    # O(n^2) when a set-based approach is O(n) — performance
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

def process(user_input):
    # eval on untrusted input — arbitrary code execution
    return eval(user_input)

class OrderProcessor:
    def __init__(self):
        self.discount = 0.1

    def apply_discount(self, price):
        # magic number, no validation that price >= 0 — maintainability
        return price - (price * self.discount)