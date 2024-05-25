import sqlite3

def init_db():
    conn = sqlite3.connect('nervousness_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Nervousness (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  weak INTEGER,
                  strong INTEGER,
                  neutral INTEGER
                  )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
