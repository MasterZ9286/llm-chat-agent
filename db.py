import sqlite3

def init_db():
    conn = sqlite3.connect("chat.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()

def save_message(session_id, role, content):
    conn = sqlite3.connect("chat.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",(session_id, role, content))
    conn.commit()
    conn.close()

def load_messages(session_id):
    conn = sqlite3.connect("chat.db")
    cur = conn.cursor()
    cur.execute("SELECT role, content FROM messages WHERE session_id = ?", (session_id,))
    rows = cur.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({"role": r[0], "content": r[1]})
    return result

def clear_messages(session_id):
    conn = sqlite3.connect("chat.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM messages WHERE session_id = ?", (session_id, ))
    conn.commit()
    conn.close()