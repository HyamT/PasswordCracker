# Hyam Cracker

Hyam Cracker is a Python-based password-cracking tool designed for educational and ethical purposes. This project demonstrates various password-cracking techniques, such as dictionary attacks, and includes advanced features like parallel processing and support for multiple hash algorithms.

🚧 **This project is a work in progress!** 🚧  
New features and enhancements are being added regularly. Stay tuned for updates.

---

## **Features**

- Dictionary-based password cracking
- Support for multiple hash algorithms:
  - MD5
  - SHA-1
  - SHA-256
- Command-line interface (CLI) for flexible use
- Real-time progress display with a progress bar
- Easy-to-read results exported to CSV

### **Planned Features**
- Parallel processing to improve performance
- Graphical user interface (GUI) with Tkinter or PyQt
- Rainbow table functionality
- Hybrid attacks (dictionary + brute-force)
- Password strength analysis and reporting
- Docker support for portability

---

## **Getting Started**

### **Prerequisites**
- Python 3.7 or higher
- Required libraries (install via `pip`):
  ```bash
  pip install argparse tqdm


Setup

Clone this repository:

git clone https://github.com/<yourusername>/hyam_cracker.git

Navigate to the project directory:

cd hyam_cracker

Run the password-cracking script:

python password_cracker_cli.py --algorithm md5 --wordlist wordlist.csv --output results.csv

Usage
Command-Line Arguments
Argument	Description	Default
--algorithm	Hash algorithm to use (e.g., md5, sha1, sha256)	md5
--wordlist	Path to the wordlist file	wordlist.csv
--output	File to save the results	results.csv
Example

python password_cracker_cli.py --algorithm sha256 --wordlist wordlist.csv --output results.csv

Disclaimer

This tool is intended for educational purposes only. Use it responsibly and ensure you have proper authorisation before testing any passwords or systems. The developer is not responsible for any misuse of this tool.
Contributing

Contributions are welcome! If you’d like to improve this project, feel free to fork the repository, create a feature branch, and submit a pull request.
Contact

For questions, feedback, or suggestions:

GitHub Issues: Open an issue in this repository.

License

This project is licensed under the MIT License.
