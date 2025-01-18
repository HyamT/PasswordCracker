import argparse
import sqlite3
import hashlib
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from tqdm import tqdm

# Define CLI arguments
parser = argparse.ArgumentParser(description="Advanced Password Cracker")
parser.add_argument("--algorithm", type=str, default="md5", help="Hash algorithm to use (md5, sha1, sha256)")
parser.add_argument("--wordlist", type=str, default="wordlist.csv", help="Path to the wordlist file")
parser.add_argument("--output", type=str, default="results.csv", help="File to save the results")
args = parser.parse_args()

# Connect to the database
conn = sqlite3.connect('password_cracker.db')
cursor = conn.cursor()

# Fetch target hashes
cursor.execute("SELECT hash FROM target_hashes")
target_hashes = [row[0] for row in cursor.fetchall()]

# Fetch words from wordlist table
cursor.execute("SELECT word FROM wordlist")
words = [row[0] for row in cursor.fetchall()]

# Function to compute hash
def compute_hash(word, algorithm='md5'):
    if algorithm == 'md5':
        return hashlib.md5(word.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(word.encode()).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(word.encode()).hexdigest()
    else:
        raise ValueError("Unsupported hash algorithm.")

# Cracking logic
cracked_passwords = []
for word in tqdm(words, desc="Cracking Progress"):
    hashed_word = compute_hash(word, args.algorithm)
    if hashed_word in target_hashes:
        print(f"Cracked! Word: {word} -> Hash: {hashed_word}")
        cracked_passwords.append((hashed_word, word))

# Save results to output file
with open(args.output, 'w') as output_file:
    output_file.write("Hash,Cracked Password\n")
    for hash_value, cracked_word in cracked_passwords:
        output_file.write(f"{hash_value},{cracked_word}\n")

print(f"Cracking completed. {len(cracked_passwords)} passwords cracked.")
