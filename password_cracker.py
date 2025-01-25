import sqlite3
import hashlib

def fetch_target_hashes(db_cursor: sqlite3.Cursor) -> list[str]:
    db_cursor.execute("SELECT hash FROM target_hashes")
    return [row[0] for row in db_cursor.fetchall()]

def fetch_target_wordlist(db_cursor: sqlite3.Cursor) -> list[str]:
    db_cursor.execute("SELECT word FROM wordlist")
    return [row[0] for row in db_cursor.fetchall()]

def generate_variations(word) -> set[str]:
    variations = set()
    variations.add(word)  # Original word
    variations.add(word.capitalize())  # Capitalised word
    variations.add(word.upper())  # Uppercase word
    variations.add(word + "123")  # Append numbers
    variations.add(word + "!")  # Append symbols
    variations.add(word.replace("a", "@").replace("o", "0"))  # Leetspeak substitutions
    return variations

def password_cracking_logic(password_list: list[str], target_hashes: list[str]) -> set[(str,str)]:
    cracked_passwords = set()
    for word in password_list:
        # Generate variations of the word
        variations = generate_variations(word)
        for variant in variations:
            # Compute hash for each variation (MD5 in this example)
            hashed_word = hashlib.md5(variant.encode()).hexdigest()

            # Check if the hash matches any target hash
            if hashed_word in target_hashes:
                cracked_passwords.add((hashed_word, variant))
    
    return cracked_passwords

def store_results_in_database(db_cursor: sqlite3.Cursor, cracked_passwords: set[(str,str)]):
    for hash_value, cracked_word in cracked_passwords:
        print(f"Cracked! Word: {cracked_word} -> Hash: {hash_value}")
        db_cursor.execute(
            "INSERT INTO results (hash, cracked_password, status) VALUES (?, ?, 'success')",
            (hash_value, cracked_word)
        )
    print(f"Cracking completed. {len(cracked_passwords)} passwords cracked.")

def update_status_for_failed_hashes(db_cursor: sqlite3.Cursor):
    db_cursor.execute("SELECT hash FROM target_hashes WHERE hash NOT IN (SELECT hash FROM results WHERE status = 'success')")
    failed_hashes = [row[0] for row in db_cursor.fetchall()]
    for failed_hash in failed_hashes:
        db_cursor.execute(
            "INSERT INTO results (hash, status) VALUES (?, 'failed')",
            (failed_hash,)
        )

def main():
    conn = sqlite3.connect('password_cracker.db')
    cursor = conn.cursor()

    target_hashes = fetch_target_hashes(cursor)
    password_list = fetch_target_wordlist(cursor)

    cracked_password = password_cracking_logic(password_list, target_hashes)
    store_results_in_database(cursor, cracked_password)
    update_status_for_failed_hashes(cursor)


    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
