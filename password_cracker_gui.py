import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import csv
from password_cracker import fetch_target_wordlist, process_word

# GUI Functions
def select_wordlist():
    filepath = filedialog.askopenfilename(title="Select Wordlist", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
    wordlist_path.set(filepath)

def start_cracking():
    # Get inputs
    wordlist_file = wordlist_path.get()
    target_hashes_input = target_hashes_text.get("1.0", tk.END).strip()
    selected_algorithm = hash_algorithm.get()

    if not wordlist_file or not target_hashes_input:
        messagebox.showerror("Error", "Please provide a wordlist and target hashes.")
        return

    # Read wordlist
    try:
        with open(wordlist_file, 'r', encoding='utf-8-sig') as file:
            words = [line.strip() for line in file]
    except Exception as e:
        messagebox.showerror("Error", f"Error reading wordlist: {e}")
        return

    # Parse target hashes
    target_hashes = [line.strip() for line in target_hashes_input.splitlines()]

    # Perform cracking
    cracked_passwords = []
    for word in words:
        hashed_word = hashlib.new(selected_algorithm, word.encode()).hexdigest()
        if hashed_word in target_hashes:
            cracked_passwords.append((hashed_word, word))

    # Display results
    result_text.delete("1.0", tk.END)
    if cracked_passwords:
        result_text.insert(tk.END, "Cracked Passwords:\n")
        for hash_value, password in cracked_passwords:
            result_text.insert(tk.END, f"{hash_value} -> {password}\n")
        save_results_to_csv(cracked_passwords)
    else:
        result_text.insert(tk.END, "No passwords cracked.")

def save_results_to_csv(results):
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filepath:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Hash", "Password"])
            writer.writerows(results)
        messagebox.showinfo("Success", f"Results saved to {filepath}")

# Main GUI
root = tk.Tk()
root.title("Password Cracker")
root.geometry("600x400")

# Wordlist Selection
wordlist_path = tk.StringVar()
tk.Label(root, text="Wordlist File:").pack(anchor="w", padx=10, pady=5)
tk.Entry(root, textvariable=wordlist_path, width=50).pack(anchor="w", padx=10)
tk.Button(root, text="Select File", command=select_wordlist).pack(anchor="w", padx=10, pady=5)

# Target Hashes Input
tk.Label(root, text="Target Hashes (one per line):").pack(anchor="w", padx=10, pady=5)
target_hashes_text = tk.Text(root, height=5, width=50)
target_hashes_text.pack(anchor="w", padx=10)

# Hash Algorithm Selection
tk.Label(root, text="Hash Algorithm:").pack(anchor="w", padx=10, pady=5)
hash_algorithm = tk.StringVar(value="md5")
tk.OptionMenu(root, hash_algorithm, "md5", "sha1", "sha256").pack(anchor="w", padx=10)

# Start Button
tk.Button(root, text="Start Cracking", command=start_cracking).pack(anchor="w", padx=10, pady=10)

# Results Display
tk.Label(root, text="Results:").pack(anchor="w", padx=10, pady=5)
result_text = tk.Text(root, height=10, width=70)
result_text.pack(anchor="w", padx=10)

root.mainloop()
