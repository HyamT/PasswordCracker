import sqlite3
import hashlib

def populate_wordlist(cursor, file_path='test_wordlist.csv'):
    """Populate the wordlist table from a CSV file."""
    with open(file_path, 'r', encoding='utf-8-sig') as wordlist_file:
        words = [(line.strip(),) for line in wordlist_file]
    cursor.executemany("INSERT INTO wordlist (word) VALUES (?)", words)
    print(f"Inserted {len(words)} words into the wordlist table.")

def populate_target_hashes(cursor, file_path='test_target_hashes.csv'):
    """Populate the target_hashes table from a CSV file."""
    with open(file_path, 'r', encoding='utf-8-sig') as target_hashes_file:
        hashes = [(line.strip(),) for line in target_hashes_file]
    cursor.executemany("INSERT INTO target_hashes (hash) VALUES (?)", hashes)
    print(f"Inserted {len(hashes)} hashes into the target_hashes table.")

def populate_rainbow_table(cursor):
    """Populate the rainbow table with precomputed hashes from the wordlist."""
    # Fetch words from the wordlist table
    cursor.execute("SELECT word FROM wordlist")
    words = [row[0] for row in cursor.fetchall()]

    # Precompute hashes and insert into the rainbow table
    print("Populating the rainbow table...")
    for word in words:
        hashed_word = hashlib.md5(word.encode()).hexdigest()
        cursor.execute("INSERT INTO rainbow_table (word, hash) VALUES (?, ?)", (word, hashed_word))
    print(f"Inserted {len(words)} entries into the rainbow table.")

def setup_database():
    """Main function to populate all necessary tables."""
    connection = sqlite3.connect('password_cracker.db')
    cursor = connection.cursor()

    # Ensure tables exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wordlist (
        word TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS target_hashes (
        hash TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rainbow_table (
        word TEXT NOT NULL,
        hash TEXT NOT NULL
    )
    """)

    # Populate the tables
    populate_wordlist(cursor)
    populate_target_hashes(cursor)
    populate_rainbow_table(cursor)

    # test
    # cursor.execute("DELETE FROM wordlist")
    # cursor.execute("DELETE FROM target_hashes")
    # connection.commit()

    connection.commit()
    connection.close()
    print("Database setup and population complete.")

if __name__ == '__main__':
    setup_database()
