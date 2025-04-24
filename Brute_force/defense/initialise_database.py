import sqlite3

# create database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# user table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# user data
users = [
    ("admin", "123456", "uceez14@ucl.ac.uk"),
    ("Kitty", "234567", "uceez14@ucl.ac.uk")
]

cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", users)

conn.commit()
conn.close()

print("Database Established：users.db")
