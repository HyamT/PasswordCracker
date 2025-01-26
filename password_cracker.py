import sqlite3
import hashlib
import logging
from multiprocessing import Pool
import csv

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("password_cracker.log"),
        logging.StreamHandler()
    ]
)

def fetch_target_hashes(db_cursor):
    logging.info("Fetching target hashes from the database...")
    db_cursor.execute("SELECT hash FROM target_hashes")
    hashes = [row[0] for row in db_cursor.fetchall()]
    logging.info(f"Fetched {len(hashes)} target hashes.")
    return hashes

def fetch_target_wordlist(db_cursor):
    logging.info("Fetching words from the wordlist...")
    db_cursor.execute("SELECT word FROM wordlist")
    words = [row[0] for row in db_cursor.fetchall()]
    logging.info(f"Fetched {len(words)} words from the wordlist.")
    return words

def generate_variations(word):
    variations = set()
    variations.add(word)
    variations.add(word.capitalize())
    variations.add(word.upper())
    variations.add(word + "123")
    variations.add(word + "!")
    variations.add(word.replace("a", "@").replace("o", "0"))
    return variations

def process_word(word, target_hashes):
    cracked = []
    variations = generate_variations(word)
    for variant in variations:
        hashed_word = hashlib.md5(variant.encode()).hexdigest()
        if hashed_word in target_hashes:
            cracked.append((hashed_word, variant))
    return cracked

def lookup_rainbow_table(db_cursor, target_hashes):
    logging.info("Looking up hashes in the rainbow table...")
    cracked = []
    for hash_value in target_hashes:
        db_cursor.execute("SELECT word FROM rainbow_table WHERE hash = ?", (hash_value,))
        result = db_cursor.fetchone()
        if result:
            cracked.append((hash_value, result[0]))
    logging.info(f"Found {len(cracked)} matches in the rainbow table.")
    return cracked

def process_chunk(chunk, target_hashes):
    cracked = []
    for word in chunk:
        cracked.extend(process_word(word, target_hashes))
    return cracked

def chunkify(lst, n):
    """Split a list into n roughly equal-sized chunks."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def password_cracking_parallel(password_list, target_hashes, num_processes=4):
    # Split the wordlist into chunks
    chunks = list(chunkify(password_list, len(password_list) // num_processes))
    # Use a multiprocessing pool to process each chunk
    with Pool(processes=num_processes) as pool:
        results = pool.starmap(process_chunk, [(chunk, target_hashes) for chunk in chunks])
    flattened_cracked_passwords = {item for sublist in results for item in sublist}  # Use a set for unique results
    return flattened_cracked_passwords

def store_results_in_database(db_cursor, cracked_passwords):
    logging.info("Storing cracked passwords in the database...")
    for hash_value, cracked_word in cracked_passwords:
        db_cursor.execute(
            "INSERT INTO results (hash, cracked_password, status) VALUES (?, ?, 'success')",
            (hash_value, cracked_word)
        )
    logging.info(f"Stored {len(cracked_passwords)} cracked passwords.")

def update_status_for_failed_hashes(db_cursor):
    db_cursor.execute("SELECT hash FROM target_hashes WHERE hash NOT IN (SELECT hash FROM results WHERE status = 'success')")
    failed_hashes = [row[0] for row in db_cursor.fetchall()]
    for failed_hash in failed_hashes:
        db_cursor.execute(
            "INSERT INTO results (hash, status) VALUES (?, 'failed')",
            (failed_hash,)
        )

def store_results_in_csv(file_path, cracked_passwords):
    """Write cracked passwords to a CSV file."""
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write header row
        writer.writerow(["Hash", "Cracked Password"])
        # Write each cracked password
        for hash_value, cracked_word in cracked_passwords:
            writer.writerow([hash_value, cracked_word])
    print(f"Results written to {file_path}")

def main():
    conn = sqlite3.connect('password_cracker.db')
    cursor = conn.cursor()

    target_hashes = fetch_target_hashes(cursor)

    # Use the rainbow table for cracking
    cracked_passwords = lookup_rainbow_table(cursor, target_hashes)
    cracked_passwords = set(cracked_passwords)  # Ensure uniqueness

    # For any remaining hashes, use real-time cracking
    remaining_hashes = set(target_hashes) - {hash_value for hash_value, _ in cracked_passwords}
    if remaining_hashes:
        logging.info(f"Falling back to real-time cracking for {len(remaining_hashes)} remaining hashes...")
        password_list = fetch_target_wordlist(cursor)
        cracked_passwords.update(password_cracking_parallel(password_list, list(remaining_hashes), num_processes=4))

    logging.info(f"Cracking completed. Total passwords cracked: {len(cracked_passwords)}.")

    # Save results to a CSV file
    store_results_in_csv('cracked_passwords.csv', cracked_passwords)

    # Optionally store results in the database
    store_results_in_database(cursor, cracked_passwords)
    update_status_for_failed_hashes(cursor)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
