import sqlite3

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        subscription_active INTEGER DEFAULT 0,
        subscription_expiry TEXT,
        discount_code TEXT
    )
    """)

    db.commit()
    db.close()
