import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL,
                      license_id TEXT NOT NULL);''')
    except sqlite3.Error as e:
        print(e)

def add_user(conn, username, license_id):
    try:
        c = conn.cursor()
        c.execute('''INSERT INTO users(username, license_id) VALUES(?, ?)''', (username, license_id))
        conn.commit()
        return c.lastrowid
    except sqlite3.Error as e:
        print(e)
    return None

def get_user_by_id(conn, user_id):
    try:
        c = conn.cursor()
        c.execute('''SELECT * FROM users WHERE id=?''', (user_id,))
        return c.fetchone()
    except sqlite3.Error as e:
        print(e)
    return None
