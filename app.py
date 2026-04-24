from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os
from werkzeug.utils import secure_filename
from PIL import Image
import secrets
import string

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

ph=PasswordHasher()

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def discount_db_for_user(username, result):
    with sqlite3.connect('DB.db') as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM users WHERE username=?', (username,))
        user_row = cursor.fetchone()

        if user_row is None:
            raise ValueError(f"User '{username}' not found")

        user_id = user_row[0]

        cursor.execute(
            '''
            INSERT OR REPLACE INTO discounts (discount_code, user_id)
            VALUES (?, ?)
            ''',
            (result, user_id)
        )


@app.route('/')
def index():

    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()

    username = session.get("username")

    cursor.execute('SELECT image FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()

    pfp = row[0] if row and row[0] else "static/images/avatars/account-pfp.png"

    cursor.execute('SELECT NAME, PRICE, IMAGE FROM items')
    products = cursor.fetchall()

    return render_template('index.html',
                            items = products,
                            pfp = pfp)

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
        preferred = "None"

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

        default_image = "static/images/avatars/account-pfp.png"

        hashed_password = ph.hash(password)
        cursor.execute('INSERT INTO users (username, password, image, preferred_address, total_orders, progress) VALUES (?, ?, ?, ?, ?, ?)', (username, hashed_password, default_image, preferred, 0, 0))
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

        formatted_file_name = product_name.replace(" ", "-")

        file = request.files.get('product_image')
        filename = "default.png"

        UPLOAD_FOLDER = 'static/images'

        if file and file.filename != '':
                img = Image.open(file)

                w,h = img.size

                left = (w // 2) - 360
                right = (w // 2) + 360

                top = (h // 2) - 640
                bottom = (h // 2) + 640

                cropped = img.crop((left, top, right, bottom))

                filename = secure_filename(formatted_file_name)  + ".png"
                filepath=os.path.join(UPLOAD_FOLDER, filename)
                cropped.save(filepath)

        cursor.execute('INSERT INTO items (NAME, PRICE, IMAGE) VALUES (?, ?, ?)',
                           (product_name, product_price, filepath))

        connection.commit()
        connection.close()

        return redirect(url_for('staff_menu'))

@app.route('/account')
def account():
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()

    username = session.get("username")

    # get user id
    cursor.execute(
        'SELECT id FROM users WHERE username = ?',
        (username,)
    )
    user_row = cursor.fetchone()
    user_id = user_row[0] if user_row else None

    # get user info
    cursor.execute(
        'SELECT image, preferred_address, total_orders FROM users WHERE username = ?',
        (username,)
    )
    user = cursor.fetchone()

    if not user:
        return "User not found", 404

    pfp = user[0] if user[0] else "static/images/avatars/account-pfp.png"
    address = user[1] if user[1] else ""
    total_orders = user[2] if user[2] is not None else 0

    # get all allergens
    cursor.execute('SELECT * FROM allergens')
    allergens = cursor.fetchall()

    # get selected allergens
    cursor.execute(
        'SELECT allergen_id FROM user_allergens WHERE user_id = ?',
        (user_id,)
    )
    user_allergens = [row[0] for row in cursor.fetchall()]

    # get progress
    cursor.execute(
        'SELECT progress FROM users WHERE id = ?',
        (user_id,)
    )
    progress = cursor.fetchone()
    progress = progress[0]

    connection.close()

    return render_template(
        'account.html',
        username=username,
        pfp=pfp,
        address=address,
        total_orders=total_orders,
        allergens=allergens,
        user_allergens=user_allergens,
        progress=progress
    )

@app.route('/changepfp', methods=['POST'])
def change_pfp():

    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()

    username = session.get("username")

    picture = request.files.get('profile_picture')

    UPLOAD_FOLDER = 'static/images/avatars'

    if picture and picture.filename != '':

        img = Image.open(picture)

        base_name = secure_filename(username)

        filename = base_name + ".png"

        filepath = os.path.join(UPLOAD_FOLDER, filename)

        img.save(filepath)

        cursor.execute(
            "UPDATE users SET image = ? WHERE username = ?",
            (filepath, username)
        )

        connection.commit()

    return redirect('/account')

@app.route('/deletepfp', methods=['POST'])
def delete_pfp():
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()

    username = session.get("username")

    DEFAULT_PFP = "static/images/avatars/account-pfp.png"

    cursor.execute(
        'SELECT image FROM users WHERE username = ?',
        (username,)
    )
    row = cursor.fetchone()

    if row and row[0] and row[0] != DEFAULT_PFP and os.path.exists(row[0]):
        os.remove(row[0])

    cursor.execute(
        'UPDATE users SET image = ? WHERE username = ?',
        (DEFAULT_PFP,username,)
    )

    connection.commit()
    connection.close()

    return redirect('/account')

@app.route('/changeusername', methods=['POST'])
def change_username():
    username = session.get("username")
    new_username = request.form.get('username')

    if new_username == username:
        flash("That's already your username.")
        return redirect('/account')

    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()

    cursor.execute('SELECT username FROM users WHERE username = ?', (new_username,))

    exists = cursor.fetchone() is not None

    if exists:
        flash("Username already taken, pick another one!")
    else:
        cursor.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, username))
        connection.commit()

        session["username"] = new_username

        flash("Username updated successfully!")

    connection.close()

    return redirect('/account')

@app.route('/changeaddress', methods=['POST'])
def change_address():
    username = session.get("username")
    street = request.form.get('street', '').strip()
    city = request.form.get('city', '').strip()
    postcode = request.form.get('postcode', '').strip()

    address = f"{street}, {city}, {postcode}"

    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE users SET preferred_address = ? WHERE username = ?', (address, username))

    connection.commit()
    connection.close()
    
    return redirect('/account')

@app.route('/addorder', methods=['POST'])
def add_order():
    username = session.get("username")
    
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()

    cursor.execute('SELECT progress FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    progress = row[0] if row else 0

    progress += 25

    if progress >= 100:
        alphabet = string.ascii_letters + string.digits
        result = ''.join(secrets.choice(alphabet) for _ in range(16))

        discount_db_for_user(username, result)
        progress = 0

    cursor.execute(
        'UPDATE users SET total_orders = total_orders + 1, progress = ? WHERE username = ?',
        (progress, username)
    )

    if progress > 100:
        alphabet = string.ascii_letters + string.digits
        result = ''.join(secrets.choice(alphabet) for _ in range(16))

        discount_db_for_user(username, result)
        progress = 0        

    connection.commit()
    connection.close()

    return redirect('/')

@app.route('/updateallergens', methods=["POST"])
def update_allergens():

    username = session.get("username")

    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM users WHERE username=?', (username,))
    user_row = cursor.fetchone()

    if user_row:
        user_id = user_row[0]
    else:
        flash("User not found.")
        return redirect('/login')
    
    selected_allergens = request.form.getlist('allergens')

    try:
        cursor.execute('DELETE FROM user_allergens WHERE user_id = ?', (user_id,))

        for allergen_id in selected_allergens:
            cursor.execute(
                'INSERT INTO user_allergens (user_id, allergen_id) VALUES (?, ?)', 
                (user_id, allergen_id)
            )
            
        connection.commit()
        flash("Allergies updated successfully!")
        
    except Exception as e:
        connection.rollback()
        flash("An error occurred.")
        print(e)
        
    finally:
        connection.close()

    return redirect('/account')

@app.route('/deleteaccount', methods=['POST'])
def delete_account():
    username = session.get("username")
    if not username:
        flash("You must be logged in to delete your account.")
        return redirect(url_for('login'))

    try:
        connection = sqlite3.connect('DB.db')
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_row = cursor.fetchone()

        if user_row:
            user_id = user_row[0]

            cursor.execute('SELECT image FROM users WHERE id = ?', (user_id,))
            image_row = cursor.fetchone()
            image_path = image_row[0] if image_row else None

            cursor.execute('DELETE FROM user_allergens WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM discounts WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))

            if image_path and os.path.exists(image_path) and image_path != "static/images/avatars/account-pfp.png":
                os.remove(image_path)
            
            connection.commit()
            connection.close()

            session.pop('username', None)
            session.pop('staff', None)
            session.pop('staff-username', None)

            flash("Your account has been deleted successfully.")
            return redirect(url_for('index'))

        else:
            flash("User not found.")
            connection.close()
            return redirect(url_for('index'))

    except Exception as e:
        connection.rollback()
        flash(f"An error occurred while deleting your account: {e}")
        return redirect(url_for('account'))

if __name__ == '__main__':
    app.run(debug=True)