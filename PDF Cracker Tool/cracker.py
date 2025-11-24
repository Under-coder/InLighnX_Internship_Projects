import itertools
import pikepdf
from tqdm import tqdm
import string
from concurrent.futures import ThreadPoolExecutor, as_completed 
import argparse

def generate_passwords(chars, min_length, max_length):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)

def load_passwords(pdf_file):
    with open(pdf_file, 'r') as file:
        for line in file:
            yield line.strip()

def try_password(pdf_file, password):
    try:
        with pikepdf.open(pdf_file, password=password) as pdf:
            print(f"[+] Password found:{password}")
            return password
    except pikepdf._core.PasswordError:
        return None


def decrypt_pdf(pdf_file, passwords, total_passwords, max_workers=4):
    with tqdm(total=total_passwords, desc="Decrypting PDF", unit='passwords') as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_password = {executor.submit(try_password, pdf_file, pwd): pwd for pwd in passwords}

            for future in tqdm(future_to_password, total=total_passwords):
                password = future_to_password[future]
                if future.result():
                    return future.result()
                pbar.update(1)
    print("Unable to decrypt the PDF. Password not found.")
    return None

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Decrypt a password-protected PDF file using brute-force or dictionary attack.")
    parser.add_argument("pdf_file", help="Path to the password-protected PDF file.")
    parser.add_argument('-w', '--wordlist', help="Path to file containing list of passwords", default=None)
    parser.add_argument('-g', '--generate', action='store_true', help="Generate passwords using brute-force method.")
    parser.add_argument('-min', '--min_length', type=int, default=1, help="Minimum length of generated passwords.")
    parser.add_argument('-max', '--max_length', type=int, default=4, help="Maximum length of generated passwords.")
    parser.add_argument('-c', '--charset', type=str, default=string.ascii_letters + string.digits + string.punctuation, help="Character set to use for password generation.")
    parser.add_argument('--max_workers', type=int, default=4, help="Maximum number of concurrent threads.")

    args = parser.parse_args()

    if args.generate:
        passwords = generate_passwords(args.charset, args.min_length, args.max_length)
        total_passwords = sum(1 for _ in generate_passwords(args.charset, args.min_length, args.max_length))
    elif args.wordlist:
        passwords = load_passwords(args.wordlist)
        total_passwords = sum(1 for _ in load_passwords(args.wordlist))
    else:
        print("Please provide either a wordlist file or enable password generation.")
        exit(1)

    decrypted_password = decrypt_pdf(args.pdf_file, passwords, total_passwords, args.max_workers)

    if decrypted_password:
        print(f"Decrypted PDF password: {decrypted_password}")
    else:
        print("Failed to decrypt the PDF.")