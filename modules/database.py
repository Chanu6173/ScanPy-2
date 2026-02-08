import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.getcwd(), 'data', 'scanpy.db')



def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_date TEXT,
            doc_type TEXT,
            extracted_text TEXT,
            structured_data TEXT,
            file_path TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_scan(filename, doc_type, extracted_text, structured_data, file_path=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('''
            INSERT INTO scans (filename, upload_date, doc_type, extracted_text, structured_data, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (filename, upload_date, doc_type, extracted_text, str(structured_data), file_path))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"DB Error: {e}")
        return False

def get_recent_scans():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM scans ORDER BY id DESC LIMIT 5')
    rows = c.fetchall()
    conn.close()
    return rows
