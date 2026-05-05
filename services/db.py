import os
import psycopg2

def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        file_url TEXT,
        paid BOOLEAN
    )
    """)

    conn.commit()
    conn.close()

def save_user(user_id, file_url):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO users (user_id, file_url, paid)
    VALUES (%s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE SET file_url=%s
    """, (user_id, file_url, False, file_url))

    conn.commit()
    conn.close()

def mark_paid(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("UPDATE users SET paid=TRUE WHERE user_id=%s", (user_id,))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    data = cur.fetchone()

    conn.close()
    return data
