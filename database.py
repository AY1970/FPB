import sqlite3

DATABASE_FILE = 'contacts.db'


def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Creating the users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      first_name TEXT,
                      last_name TEXT,
                      phone_number TEXT)''')

    conn.commit()
    conn.close()


def add_user(first_name, last_name, phone_number):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Inserting a new user into the users table
    cursor.execute('''INSERT INTO users (first_name, last_name, phone_number)
                      VALUES (?, ?, ?)''', (first_name, last_name, phone_number))

    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Getting all users from the users table
    cursor.execute('''SELECT * FROM users''')
    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_user(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Removing a user from the users table by his id
    cursor.execute('''DELETE FROM users WHERE id = ?''', (user_id,))

    conn.commit()
    conn.close()

