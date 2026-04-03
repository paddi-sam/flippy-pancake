from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

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

        hashed_input = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if row and row[0] == hashed_input:
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

        print("Registering:", username, password, confirm_password)  

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
        

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
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

        hashed_input = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if row and row[0] == hashed_input:
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

@app.route('/staffmenu')
def staff_menu():
    if not session.get('staff'):
        flash("You need to be staff to see this")
        return redirect(url_for('stafflogin'))
    else:
        return render_template('staff-menu.html')

if __name__ == '__main__':
    app.run(debug=True)