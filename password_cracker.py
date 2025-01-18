import sqlite3
import hashlib

# Connect to the database
conn = sqlite3.connect('password_cracker.db')
cursor = conn.cursor()

# Fetch target hashes
cursor.execute("SELECT hash FROM target_hashes")
target_hashes = [row[0] for row in cursor.fetchall()]

# Fetch words from wordlist
cursor.execute("SELECT word FROM wordlist")
words = [row[0] for row in cursor.fetchall()]

# Cracking logic
cracked_passwords = []
for word in words:
    # Compute hash for the word (MD5 in this example)
    hashed_word = hashlib.md5(word.encode()).hexdigest()  # Replace MD5 with other algorithms as needed

    # Check if the hash matches any target hash
    if hashed_word in target_hashes:
        print(f"Cracked! Word: {word} -> Hash: {hashed_word}")
        cracked_passwords.append((hashed_word, word))

# Store results in the database
for hash_value, cracked_word in cracked_passwords:
    cursor.execute(
        "INSERT INTO results (hash, cracked_password, status) VALUES (?, ?, 'success')",
        (hash_value, cracked_word)
    )

# Update status for failed hashes
cursor.execute("SELECT hash FROM target_hashes WHERE hash NOT IN (SELECT hash FROM results WHERE status = 'success')")
failed_hashes = [row[0] for row in cursor.fetchall()]
for failed_hash in failed_hashes:
    cursor.execute(
        "INSERT INTO results (hash, status) VALUES (?, 'failed')",
        (failed_hash,)
    )

conn.commit()
conn.close()

print(f"Cracking completed. {len(cracked_passwords)} passwords cracked.")