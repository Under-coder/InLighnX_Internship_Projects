import PyPDF2, sys
from PyPDF2 import PdfReader, PdfWriter

def create_password_protected_pdf(input_pdf, output_pdf, password):
    try:
       # Create a PDF reader object
       reader = PdfReader(input_pdf)
       
       # Create a PDF writer object
       writer = PdfWriter()
       
       # Add all pages from the reader to the writer
       for page in range(len(reader.pages)):
           writer.add_page(reader.pages[page])
       
       # Encrypt the PDF with the provided password
       writer.encrypt(password)
       
       # Write the encrypted PDF to a new file
       with open(output_pdf, 'wb') as output_file:
           writer.write(output_file)
       
       print(f"Password-protected PDF created successfully: {output_pdf}")

    except Exception as e:
        print(f"An error occurred: {e}")
    except FileNotFoundError:
        print(f"The file {input_pdf} was not found.")
    except PyPDF2.utils.PdfReadError:
        print(f"The file {input_pdf} is not a valid PDF.")


def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <input_pdf> <output_pdf> <password>")
        return
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    password = sys.argv[3]
    
    create_password_protected_pdf(input_pdf, output_pdf, password)

if __name__ == "__main__":
    main()
