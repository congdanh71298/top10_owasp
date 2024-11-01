from flask import Flask, request, render_template_string, redirect, url_for, session
import sqlite3
import hashlib
import os
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
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

# Patched version with access control
@app.route('/user_secure')
def user_profile_secure():
    if 'username' in session:
        username = session['username']
        return f"Welcome, {username}!"
    else:
        return redirect(url_for('login'))

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
    return render_template_string('''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit">
        </form>
    ''')

# Patched version with hashed passwords
@app.route('/register_secure', methods=['GET', 'POST'])
def register_secure():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Secure code: Hashing passwords
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return "User registered securely."
    return render_template_string('''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit">
        </form>
    ''')

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
    return render_template_string('''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit">
        </form>
    ''')

# Patched version with parameterized queries
@app.route('/login_secure', methods=['GET', 'POST'])
def login_secure():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Secure code: Parameterized query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = user[1]
            return redirect(url_for('user_profile_secure'))
        else:
            return "Invalid credentials."
    return render_template_string('''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit">
        </form>
    ''')

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

# Patched version with input validation
@app.route('/checkout_secure', methods=['GET', 'POST'])
def checkout_secure():
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = request.form['quantity']
        # Secure code: Validate input
        if not quantity.isdigit() or int(quantity) <= 0:
            return "Invalid quantity."
        quantity = int(quantity)
        price = get_item_price(item_id)
        total = price * quantity
        return f"Total price: ${total}"

# A05:2021 - Security Misconfiguration
@app.route('/debug')
def debug():
    # Vulnerable code: Debug mode enabled in production
    return "Debug info: " + str(session)

# Patched version with debug mode disabled
# Note: Set debug=False in app.run()
@app.route('/debug_secure')
def debug_secure():
    return "Debug mode is disabled."

# A06:2021 - Vulnerable and Outdated Components
@app.route('/legacy')
def legacy():
    # Vulnerable code: Using outdated library function
    data = request.args.get('data')
    hashed = hashlib.md5(data.encode()).hexdigest()
    return f"MD5 Hash: {hashed}"

# Patched version using updated components
@app.route('/legacy_secure')
def legacy_secure():
    data = request.args.get('data')
    # Secure code: Use SHA-256 instead of MD5
    hashed = hashlib.sha256(data.encode()).hexdigest()
    return f"SHA-256 Hash: {hashed}"

# A07:2021 - Identification and Authentication Failures
@app.route('/admin')
def admin():
    # Vulnerable code: Missing authentication
    return "Welcome to the admin panel."

# Patched version with authentication
@app.route('/admin_secure')
def admin_secure():
    if 'username' in session and session['username'] == 'admin':
        return "Welcome to the admin panel, admin."
    else:
        return redirect(url_for('login_secure'))

# A08:2021 - Software and Data Integrity Failures
@app.route('/update', methods=['POST'])
def update():
    # Vulnerable code: Unverified file upload
    file = request.files['file']
    file.save(f"./updates/{file.filename}")
    return "File uploaded."

# Patched version with file verification
@app.route('/update_secure', methods=['POST'])
def update_secure():
    file = request.files['file']
    # Secure code: Verify file type
    if allowed_file(file.filename):
        file.save(f"./updates/{secure_filename(file.filename)}")
        return "File uploaded securely."
    else:
        return "Invalid file type."

# A09:2021 - Security Logging and Monitoring Failures
@app.route('/login_attempt', methods=['POST'])
def login_attempt():
    username = request.form['username']
    password = request.form['password']
    # Vulnerable code: No logging of login attempts
    # ...existing login logic...

# Patched version with logging
@app.route('/login_attempt_secure', methods=['POST'])
def login_attempt_secure():
    username = request.form['username']
    password = request.form['password']
    # Secure code: Log login attempts
    logging.info(f"Login attempt for user: {username}")
    # ...existing login logic...

# A10:2021 - Server-Side Request Forgery (SSRF)
@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    # Vulnerable code: No validation on the URL
    response = requests.get(url)
    return response.content

# Patched version with URL validation
@app.route('/fetch_secure')
def fetch_secure():
    url = request.args.get('url')
    # Secure code: Validate URL
    if not is_allowed_domain(url):
        return "Invalid URL."
    response = requests.get(url)
    return response.content

# Additional routes for other OWASP Top 10 issues can be implemented similarly.

if __name__ == '__main__':
    app.run(debug=False)
