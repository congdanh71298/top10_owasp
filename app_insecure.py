from flask import Flask, request, render_template_string, redirect, url_for, session
import sqlite3
import os
from templates.views import LOGIN_FORM, REGISTER_FORM, CHECKOUT_FORM, UPDATE_FORM

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database_insecure.db')
    return conn

# A01:2021 - Broken Access Control
@app.route('/user/<username>')
def user_profile(username):
    # Vulnerable code: No access control
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return f"Welcome, {user[1]}!"
    else:
        return "User not found."

# A02:2021 - Cryptographic Failures
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Vulnerable code: Storing passwords in plain text
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return "User registered."
    return render_template_string(REGISTER_FORM)

# A03:2021 - Injection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Vulnerable code: SQL Injection
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = user[1]
            return redirect(url_for('user_profile', username=user[1]))
        else:
            return "Invalid credentials."
    return render_template_string(LOGIN_FORM)

# A04:2021 - Insecure Design
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = int(request.form['quantity'])
        # Vulnerable code: No validation on quantity
        price = get_item_price(item_id)
        total = price * quantity
        return f"Total price: ${total}"
    return render_template_string(CHECKOUT_FORM)

# A05:2021 - Security Misconfiguration
@app.route('/debug')
def debug():
    # Vulnerable code: Debug mode enabled in production
    return "Debug info: " + str(session)

# A06:2021 - Vulnerable and Outdated Components
@app.route('/legacy')
def legacy():
    # Vulnerable code: Using outdated library function
    data = request.args.get('data')
    hashed = hashlib.md5(data.encode()).hexdigest()
    return f"MD5 Hash: {hashed}"

# A07:2021 - Identification and Authentication Failures
@app.route('/admin')
def admin():
    # Vulnerable code: Missing authentication
    return "Welcome to the admin panel."

# A08:2021 - Software and Data Integrity Failures
@app.route('/update', methods=['POST'])
def update():
    # Vulnerable code: Unverified file upload
    file = request.files['file']
    file.save(f"./updates/{file.filename}")
    return render_template_string(UPDATE_FORM)

# A09:2021 - Security Logging and Monitoring Failures
@app.route('/login_attempt', methods=['POST'])
def login_attempt():
    username = request.form['username']
    password = request.form['password']
    # Vulnerable code: No logging of login attempts
    # ...existing login logic...

# A10:2021 - Server-Side Request Forgery (SSRF)
@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    # Vulnerable code: No validation on the URL
    response = requests.get(url)
    return response.content

if __name__ == '__main__':
    app.run(port=5001, debug=False)