from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

ph=PasswordHasher()

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = sqlite3.connect('DB.db')
        cursor = connection.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        connection.close()

        valid_password = False
        if row:
            try:
                valid_password = ph.verify(row[0], password)
            except VerifyMismatchError:
                valid_password = False

        if valid_password:
            session['username'] = username
            session['staff'] = False
            flash(f'Welcome back, {username}!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not password or not confirm_password:
            flash('All fields are required!')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match!')
            return render_template('register.html')

        if len(password) < 8:
            flash("Password too short!")
            return render_template('register.html')

        num_count = 0
        for i in password:
            if i.isdigit() == True:
                num_count += 1
        if num_count < 3:
            flash("Password needs to have 3 numbers!")
            return render_template('register.html')

        special_chars = set("!@#$%^&*()-_=+[]{};:'\",.<>/?\\|")
        special_count = 0
        for i in password:
            if i in special_chars:
                special_count += 1
        if special_count < 1:
            flash("Password must contain a special character")
            return render_template('register.html')

        connection = sqlite3.connect('DB.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            connection.close()
            flash('Username already taken!')
            return render_template('register.html')

        hashed_password = ph.hash(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        connection.commit()
        connection.close()

        flash(f'Registration successful! Welcome, {username}!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/staff-login', methods=['GET', 'POST'])
def stafflogin():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = sqlite3.connect('DB.db')
        cursor = connection.cursor()
        cursor.execute('SELECT password FROM staff WHERE username = ?', (username,))
        row = cursor.fetchone()
        connection.close()

        valid_password = False
        if row:
            try:
                valid_password = ph.verify(row[0], password)
            except VerifyMismatchError:
                valid_password = False

        if valid_password:
            session['username'] = username
            session['staff'] = True
            session['staff-username'] = username
            flash(f'Welcome back, {username}!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return render_template('staff-login.html')

    return render_template('staff-login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('staff', None)
    session.pop('staff-username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/staffmenu', methods=['GET', 'POST'])
def staff_menu():
    if not session.get('staff'):
        flash("You need to be staff to see this")
        return redirect(url_for('stafflogin'))

    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()

    current_username = session.get('username')
    cursor.execute('SELECT id FROM staff WHERE username = ?', (current_username,))
    current_user_row = cursor.fetchone()
    current_user_id = current_user_row[0] if current_user_row else None

    cursor.execute('SELECT id, username FROM staff')
    users = cursor.fetchall()

    cursor.execute('SELECT id FROM staff ORDER BY id ASC LIMIT 1')
    first_user = cursor.fetchone()
    first_user_id = first_user[0] if first_user else None

    cursor.execute('SELECT ITEM_ID, NAME, PRICE FROM items')
    items = cursor.fetchall()

    connection.close()

    return render_template('staff-menu.html',
                           users=users,
                           first_user_id=first_user_id,
                           current_user_id=current_user_id,
                           items=items)

@app.route('/staffregister', methods=['GET', 'POST'])
def staff_register():
    if request.method == 'POST':
        staff_username = request.form.get('username')
        staff_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not staff_username or not staff_password or not confirm_password:
            flash('All fields are required!')
            return redirect(url_for('staff_menu'))

        if staff_password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('staff_menu'))

        if len(staff_password) < 8:
            flash("Password too short!")
            return redirect(url_for('staff_menu'))

        num_count = 0
        for i in staff_password:
            if i.isdigit():
                num_count += 1
        if num_count < 3:
            flash("Password needs to have 3 numbers!")
            return redirect(url_for('staff_menu'))

        special_chars = set("!@#$%^&*()-_=+[]{};:'\",.<>/?\\|")
        special_count = 0
        for i in staff_password:
            if i in special_chars:
                special_count += 1
        if special_count < 1:
            flash("Password must contain a special character")
            return redirect(url_for('staff_menu'))

        connection = sqlite3.connect('DB.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM staff WHERE username = ?', (staff_username,))
        existing_user = cursor.fetchone()

        if existing_user:
            connection.close()
            flash('Username already taken!')
            return redirect(url_for('staff_menu'))
        hashed_password = ph.hash(staff_password)
        cursor.execute('INSERT INTO staff (username, password) VALUES (?, ?)', (staff_username, hashed_password))
        connection.commit()
        connection.close()

        flash('Staff added')
        return redirect(url_for('staff_menu'))


@app.route('/delete_staff', methods=['POST'])
def delete_staff():
    user_id = request.form.get('user_id')

    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM staff ORDER BY id ASC LIMIT 1')
    first_user = cursor.fetchone()

    if first_user and str(first_user[0]) == str(user_id):
        flash("You can't delete the first staff user!")
        connection.close()
        return redirect(url_for('staff_menu'))

    cursor.execute('DELETE FROM staff WHERE id = ?', (user_id,))
    connection.commit()
    connection.close()

    return redirect(url_for('staff_menu'))

@app.route('/delete_item', methods=['POST'])
def delete_item():
    item_id = request.form.get('ITEM_ID')

    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM items WHERE ITEM_ID = ?', (item_id,))
    connection.commit()
    connection.close()

    return redirect(url_for('staff_menu'))

@app.route('/additem', methods=['POST'])
def add_item():

        connection = sqlite3.connect('DB.db')
        cursor = connection.cursor()

        product_name = request.form.get('product_name')
        product_price = request.form.get('price')

        file = request.files.get('product_image')
        filename = "default.png"

        if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor.execute('INSERT INTO items (NAME, PRICE, IMAGE) VALUES (?, ?, ?)',
                           (product_name, product_price, filename))

        connection.commit()
        connection.close()

        return redirect(url_for('staff_menu'))

@app.route('/tailwind')
def tailwind():
    return render_template('tailwind.html')

if __name__ == '__main__':
    app.run(debug=True)