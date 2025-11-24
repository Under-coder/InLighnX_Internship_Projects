**PDF Password Protector**

This program creates a password-protected version of any existing PDF file.
It reads the original PDF, copies all its pages into a new file, encrypts it using the provided password, and saves the protected output.
_______________________________________________
**How it works**

- Reads the input PDF using PyPDF2
- Copies every page into a new PDF writer
- Encrypts the new PDF with the password provided in the command line
- Saves the final password-protected PDF to the specified output file
