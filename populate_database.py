import sqlite3
import csv

connection = sqlite3.connect('password_cracker.db')
cursor = connection.cursor()

with open('wordlist.csv', 'r') as wordlist_file:
    reader = csv.reader(wordlist_file)
    words = [(row[0],) for row in reader]

cursor.executemany("INSERT INTO wordlist (word) VALUES (?)", words)

print(f"Inserted {len(words)} words into the wordlist table.")

# You can repeat this structure for hashes if needed
connection.commit()
connection.close()
    