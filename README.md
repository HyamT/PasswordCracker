Hyam Cracker

Hyam Cracker is a Python-based password-cracking tool designed for educational and ethical purposes. This project demonstrates various password-cracking techniques, such as dictionary attacks, and now includes advanced features like parallel processing, rainbow tables, and a graphical user interface (GUI).

🚧 This project is actively under development! 🚧
New features and enhancements are being added regularly. Stay tuned for updates.
Features

    Dictionary-based password cracking: Uses a wordlist to efficiently crack passwords.
    Support for multiple hash algorithms:
        MD5
        SHA-1
        SHA-256
    Parallel processing: Speeds up cracking by leveraging multiple CPU cores.
    Rainbow table functionality: Precomputed hash lookups for faster results.
    Graphical user interface (GUI):
        Built with Tkinter for a user-friendly interface.
        Allows users to select wordlists, input target hashes, choose hash algorithms, and view results.
    Results exported to CSV: Easy-to-read results for further analysis.
    Command-line interface (CLI): Flexible for power users.

Planned Features

    Hybrid attacks (dictionary + brute-force combinations).
    Password strength analysis and reporting.
    Docker support for portability and ease of deployment.
    Support for additional hash algorithms (e.g., bcrypt, PBKDF2).

Getting Started
Prerequisites

    Python 3.7 or higher
    Required libraries (install via pip):

    pip install argparse tqdm hashlib tkinter

Setup

    Clone this repository:

git clone https://github.com/<your-username>/hyam_cracker.git

Navigate to the project directory:

cd hyam_cracker

Populate the database:

python populate_database.py

Run the GUI:

python password_cracker_gui.py

(Optional) Run the CLI:

    python password_cracker.py --algorithm md5 --wordlist test_wordlist.csv --output results.csv

Usage
Command-Line Arguments
Argument	Description	Default
--algorithm	Hash algorithm to use (e.g., md5, sha1, sha256).	md5
--wordlist	Path to the wordlist file.	wordlist.csv
--output	File to save the results.	results.csv
Example

python password_cracker.py --algorithm sha256 --wordlist wordlist.csv --output results.csv

GUI Usage

    Launch the GUI with:

    python password_cracker_gui.py

    Select a wordlist file: Browse and upload a CSV containing your wordlist.
    Enter target hashes: Paste your target hashes, one per line.
    Choose a hash algorithm: Select MD5, SHA-1, or SHA-256 from the dropdown menu.
    Click Start Cracking to begin, and view the results in the GUI or save them to a CSV file.

Testing

Use the provided example wordlist and hashes in the test_wordlist.csv and test_target_hashes.csv files to test the tool. Ensure that the database is properly populated by running:

python populate_database.py

Disclaimer

This tool is intended for educational purposes only. Always ensure you have proper authorisation before testing passwords or systems. Misuse of this tool is strictly prohibited, and the developer is not responsible for any improper use.
Contributing

Contributions are welcome! If you’d like to improve this project:

    Fork the repository.
    Create a feature branch:

    git checkout -b feature-name

    Submit a pull request.

Contact

For questions, feedback, or suggestions:

    GitHub Issues: Open an issue in this repository.

License

This project is licensed under the MIT License.
