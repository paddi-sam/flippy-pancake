import sqlite3
from argon2 import PasswordHasher

ph=PasswordHasher()

print(r"""
  ______ _ _                         _         __  __       _       _        _
 |  ____| (_)                       | |       / _|/ _|     | |     | |      | |
 | |__  | |_ _ __  _ __  _   _   ___| |_ __ _| |_| |_    __| | __ _| |_ __ _| |__   __ _ ___  ___
 |  __| | | | '_ \| '_ \| | | | / __| __/ _` |  _|  _|  / _` |/ _` | __/ _` | '_ \ / _` / __|/ _ \
 | |    | | | |_) | |_) | |_| | \__ \ || (_| | | | |   | (_| | (_| | || (_| | |_) | (_| \__ \  __/
 |_|    |_|_| .__/| .__/ \__, | |___/\__\__,_|_| |_|    \__,_|\__,_|\__\__,_|_.__/ \__,_|___/\___|
            | |   | |     __/ |
            |_|   |_|    |___/                                                                    """)

conn = sqlite3.connect('DB.db')
cursor = conn.cursor()

allergens = ["celery", "gluten", "crustaceans","eggs","fish","lupin","milk","molluscs","mustard","nuts","peanuts","sesame seeds","soya","sulphites"]

cursor.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

def staff_username():
    flag = True
    while flag:

        staff_user = input("Enter the staff username you want: ")
        if staff_user == "":
            print("Please type a valid username")
        else:
            flag = False
            return staff_user

def staff_pass():
    while True:

        password_score = 0
        staff_password = input("Enter the staff Password you want: ")

        special_chars = set("!@#$%^&*()-_=+[]{};:'\",.<>/?\\|")

        if any(char.isdigit() for char in staff_password):
            password_score += 1
        if any(char.isupper() for char in staff_password):
            password_score += 1
        if any(char.islower() for char in staff_password):
            password_score += 1
        if any(char in special_chars for char in staff_password):
            password_score += 1
        if len(staff_password) > 8:
            password_score += 1

        if password_score >= 3:
            print("Valid password, creating user")
            return staff_password
        else:
            print("Password too weak, try again")

valid_user = staff_username()
valid_pass = staff_pass()

hashed_staff_password = ph.hash(valid_pass)

try:
    cursor.execute('INSERT INTO staff (username, password) VALUES (?,?)',
                   (valid_user, hashed_staff_password))
    print("Staff table successfully created")

except sqlite3.IntegrityError:
    pass

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        image TEXT NOT NULL,
        preferred_address TEXT NOT NULL,
        total_orders INTEGAR NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        image TEXT NOT NULL
    )
''')

try:
    # UNCOMMENT IF YOU WANT STARTING PRODUCTS

    cursor.execute('INSERT INTO items (item_id, name, price, image) VALUES (?,?,?,?)',
                   (1, 'Berries & Cream', 5.49, 'static/images/berries-cream.jpg'))

    cursor.execute('INSERT INTO items (item_id, name, price, image) VALUES (?,?,?,?)',
                   (2, 'Chocolate Stack', 6.99, 'static/images/Chocolate-pancakes.jpg'))

    cursor.execute('INSERT INTO items (item_id, name, price, image) VALUES (?,?,?,?)',
                   (3, 'Lemon and syrup', 6.49, 'static/images/lemon-pancakes.jpg'))

    cursor.execute('INSERT INTO items (item_id, name, price, image) VALUES (?,?,?,?)',
                   (4, 'Strawberry and sauce', 7.49, 'static/images/strawberry-pancakes.jpg'))

    cursor.execute('INSERT INTO items (item_id, name, price, image) VALUES (?,?,?,?)',
                   (5, 'Gluten free', 6.49, 'static/images/glutenfree-stack.jpg'))

    print("Products successfully created")

except sqlite3.IntegrityError:
    pass

cursor.execute('''
    CREATE TABLE IF NOT EXISTS allergens(
        allergen_id INTEGER PRIMARY KEY AUTOINCREMENT,
        allergen_name STRING NOT NULL
    )
''')


for i in allergens:
    try:
        cursor.execute('INSERT INTO allergens (allergen_name) VALUES (?)', (i,))
    except sqlite3.IntegrityError:
        pass

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_allergens (
        user_id INTEGER NOT NULL,
        allergen_id INTEGER NOT NULL,
        PRIMARY KEY (user_id, allergen_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (allergen_id) REFERENCES allergens(allergen_id)
    )
''')
        
conn.commit()
conn.close()