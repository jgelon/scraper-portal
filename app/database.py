import sqlite3

DB_NAME = 'scraper.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            selector1 TEXT,
            selector2 TEXT,
            selector3 TEXT,
            last_value1 TEXT,
            last_value2 TEXT,
            last_value3 TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(url, selector1, selector2, selector3):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO entries (url, selector1, selector2, selector3)
        VALUES (?, ?, ?, ?)
    ''', (url, selector1, selector2, selector3))
    conn.commit()
    conn.close()

def get_all_entries():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM entries')
    rows = c.fetchall()
    conn.close()
    return rows

def update_last_values(entry_id, value1, value2, value3):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE entries
        SET last_value1 = ?, last_value2 = ?, last_value3 = ?
        WHERE id = ?
    ''', (value1, value2, value3, entry_id))
    conn.commit()
    conn.close()

def get_entry_by_id(entry_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    row = c.fetchone()
    conn.close()
    return row

def update_entry(entry_id, url, selector1, selector2, selector3):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE entries
        SET url = ?, selector1 = ?, selector2 = ?, selector3 = ?
        WHERE id = ?
    ''', (url, selector1, selector2, selector3, entry_id))
    conn.commit()
    conn.close()

def delete_entry(entry_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()
