import sqlite3

conn = sqlite3.connect('DB.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
''')

try:
    cursor.execute('INSERT INTO items (item_id, name, price) VALUES (?,?,?)',
                   (1, 'Berries & Cream', 5.49))
    cursor.execute('INSERT INTO items (item_id, name, price) VALUES (?,?,?)',
                   (2, 'Chocolate Stack', 6.99))
    cursor.execute('INSERT INTO items (item_id, name, price) VALUES (?,?,?)',
                   (3, 'Lemon and syrup', 6.49))
    cursor.execute('INSERT INTO items (item_id, name, price) VALUES (?,?,?)',
                   (4, 'Strawberry and sauce', 7.49))
    cursor.execute('INSERT INTO items (item_id, name, price) VALUES (?,?,?)',
                   (5, 'Gluten free', 6.49))
    
except sqlite3.IntegrityError:
    pass

cursor.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

try:
    cursor.execute('INSERT INTO staff (username, password) VALUES (?,?)',
                   ('admin', 'password123'))
    cursor.execute('INSERT INTO staff (username, password) VALUES (?,?)',
                   ('staff', 'flippy2024'))

except sqlite3.IntegrityError:
    pass

conn.commit()
conn.close()