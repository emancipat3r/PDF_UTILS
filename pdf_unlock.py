#!/usr/bin/python3

import PyPDF2
import argparse
from tqdm import tqdm

# Create the parser
parser = argparse.ArgumentParser(description='Decrypt a password-protected PDF.')

# Add the arguments
parser.add_argument('Password', metavar='password', type=str, help='the password for the PDF')
parser.add_argument('File', metavar='file', type=str, help='the path to the PDF')

# Parse the arguments
args = parser.parse_args()

# Open the PDF
pdf_file = open(args.File, 'rb')

# Create a PDF file reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# If the PDF is encrypted
if pdf_reader.is_encrypted:
    # Try to unlock the PDF with the password
    try:
        pdf_reader.decrypt(args.Password)
        print('[+] File unlocked with password')
    except:
        print('[-] Failed to decrypt the file.')
else:
    print('[-] Error - exiting')

# Create a PDF writer object
pdf_writer = PyPDF2.PdfWriter()

# Get the total number of pages
total_pages = len(pdf_reader.pages)

# Add each page in the original PDF to the writer object
for page_num in tqdm(range(total_pages), desc="[*] Processing pages"):
    page = pdf_reader.pages[page_num]
    pdf_writer.add_page(page)

# Write the pages to a new PDF
with open('unlocked.pdf', 'wb') as f:
    pdf_writer.write(f)

# Close the PDF file
print('[+] PDF unlocked - look for "unlocked.pdf" in your current path')
pdf_file.close()
