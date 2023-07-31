
#!/usr/bin/python3

import PyPDF2
import argparse
import os
from tqdm import tqdm

# Create the parser
parser = argparse.ArgumentParser(description='Decrypt password-protected PDFs.')

# Add the arguments
parser.add_argument('--pass_file', '-p', metavar='password_file', type=str, help='the file containing the password for the PDFs')
parser.add_argument('--file', '-f', metavar='files', nargs='+', type=str, help='the paths to the PDFs')

# Parse the arguments
args = parser.parse_args()

# Read the password from the file
with open(args.pass_file, 'r') as f:
    password = f.read().strip()

# Loop over each file
for file_path in args.file:
    # Open the PDF
    pdf_file = open(file_path, 'rb')

    # Create a PDF file reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # If the PDF is encrypted
    if pdf_reader.is_encrypted:
        # Try to unlock the PDF with the password
        try:
            pdf_reader.decrypt(password)
            print(f'[+] {file_path} unlocked with password')
        except:
            print(f'[-] Failed to decrypt {file_path}.')
    else:
        print(f'[-] {file_path} is not encrypted - skipping.')

    # Create a PDF writer object
    pdf_writer = PyPDF2.PdfWriter()

    # Get the total number of pages
    total_pages = len(pdf_reader.pages)

    # Add each page in the original PDF to the writer object
    for page_num in tqdm(range(total_pages), desc=f"[*] Processing pages of {file_path}"):
        page = pdf_reader.pages[page_num]
        pdf_writer.add_page(page)

    # Create the output filename by adding '_Unlocked' before the file extension
    base_name, extension = os.path.splitext(file_path)
    output_file_name = f"{base_name}_Unlocked{extension}"

    # Write the pages to the new PDF
    with open(output_file_name, 'wb') as f:
        pdf_writer.write(f)

    print(f'[+] PDF unlocked - saved as {output_file_name}')

    # Close the PDF file
    pdf_file.close()
