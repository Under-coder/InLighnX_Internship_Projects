**PDF Password Cracker**
-----------------------------------------------

This program attempts to decrypt a password-protected PDF using either a brute-force attack (automatic password generation) or a dictionary attack (wordlist).
It tries each password, checks if it can open the PDF, and stops immediately when the correct one is found.

-------------------------------------------

**How it works**

- Accepts a PDF file as input
- Uses either:

  - A wordlist supplied by the user, or
  - A brute-force generator that creates passwords of varying lengths

- Tries each password using pikepdf
- Displays progress using tqdm
- Uses multithreading for faster password attempts
- Stops and prints the password as soon as one succeeds
