import sqlite3
import os

db_file = 'database.db'

# Check if database file exists
if not os.path.exists(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Seed data
    cursor.execute('''
        INSERT INTO users (username, password) VALUES
        ('user1', 'password1'),
        ('user2', 'password2'),
        ('user3', 'password3')
    ''')

    conn.commit()
    conn.close()
else:
    print(f"Database '{db_file}' already exists.")
