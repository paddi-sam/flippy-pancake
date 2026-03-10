import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

try:
    cursor.execute('INSERT INTO users (username, password) VALUES (?,?)',
                   ('admin', 'password123'))
    cursor.execute('INSERT INTO users (username, password) VALUES (?,?)',
                   ('staff', 'flippy2024'))



except sqlite3.IntegrityError:
    pass

conn.commit()
conn.close()