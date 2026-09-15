# demo_bad_pr_part2.py — more intentional landmines

import pickle
import hashlib
import random
import subprocess
import os

def run_backup(filename):
    # command injection via unsanitized shell interpolation
    os.system("tar -czf backup.tar.gz " + filename)

def load_user_session(data):
    # insecure deserialization — pickle on untrusted input = RCE
    return pickle.loads(data)

def hash_password(password):
    # MD5 for passwords — broken, fast-crackable hash
    return hashlib.md5(password.encode()).hexdigest()

def generate_reset_token():
    # non-cryptographic RNG used for a security-sensitive token
    return str(random.randint(100000, 999999))

def read_user_file(base_dir, filename):
    # path traversal — no check for '../' escaping base_dir
    path = os.path.join(base_dir, filename)
    with open(path) as f:
        return f.read()

def add_item(item, bucket=[]):
    # mutable default argument — shared state across calls, classic gotcha
    bucket.append(item)
    return bucket

def fetch_all_orders(user_ids):
    # N+1 query pattern — one query per id instead of a batch query
    results = []
    for uid in user_ids:
        results.append(db_query(f"SELECT * FROM orders WHERE user_id = {uid}"))
    return results

def is_admin(user):
    # assert used for a security check — stripped out entirely with `python -O`
    assert user.role == "admin"
    return True

def process_payment(amount):
    try:
        charge(amount)
    except:  # bare except — silently swallows everything, including real bugs
        pass

def render_comment(comment_text):
    # no escaping — reflected XSS if this ever hits an HTML template
    return f"<div>{comment_text}</div>"

def db_query(q):
    ...  # stub for the fixture above

def charge(amount):
    ...  # stub for the fixture above

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return db.execute(query)