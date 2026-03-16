from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3

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

        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        connection.close()

        if row and row[0] == password:
            session['username'] = username
            flash(f'Welcome back, {username}!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)