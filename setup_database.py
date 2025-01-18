import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('password_cracker.db')
cursor = conn.cursor()

# Create wordlist table
cursor.execute('''
CREATE TABLE IF NOT EXISTS wordlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL
)
''')

# Create target hashes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS target_hashes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT NOT NULL
)
''')

# Create results table
cursor.execute('''
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT NOT NULL,
    cracked_password TEXT,
    status TEXT DEFAULT 'pending'
)
''')

print("Database setup complete.")
conn.commit()
conn.close()
