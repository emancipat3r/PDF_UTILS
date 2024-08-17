#!/usr/bin/python3
import PyPDF2
import argparse
import os
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich.console import Console
from rich.logging import RichHandler
import logging

# Configure logging with Rich
console = Console()
logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console)]
)
logger = logging.getLogger("pdf_unlock")

def log_info(message):
    logger.debug(f"{message}")

def log_success(message):
    logger.info(f"{message}")

def log_error(message):
    logger.error(f"{message}")

# Create the parser
parser = argparse.ArgumentParser(description='Decrypt password-protected PDFs.')
parser.add_argument('--pass_file', '-p', metavar='password_file', type=str, required=True, help='File containing the password for the PDFs')
parser.add_argument('--file', '-f', metavar='files', nargs='+', type=str, required=True, help='Path(s) to the PDFs')
parser.add_argument('--output_dir', '-o', metavar='output_directory', type=str, required=True, help='Directory to save decrypted PDFs')

# Parse the arguments
args = parser.parse_args()

# Ensure the output directory exists
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

# Read the password from the file
with open(args.pass_file, 'r') as f:
    password = f.read().strip()

# Function to process PDFs
def process_pdf(file_path):
    
    try:
        pdf_file = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        if pdf_reader.is_encrypted:
            if pdf_reader.decrypt(password):
                return pdf_reader, pdf_file
            else:
                log_error(f'Incorrect password for {file_path}')
                pdf_file.close()
        else:
            log_info(f'{file_path} is not encrypted - skipping')
            pdf_file.close()
    except Exception as e:
        log_error(f'Error processing {file_path}: {str(e)}')
        pdf_file.close()
    return None, None
        
# Function to save PDF with a new name
def save_pdf(pdf_writer, output_file_name):
    base_name = os.path.basename(file_path)
    output_file_name = os.path.join(args.output_dir, f"{os.path.splitext(base_name)[0]}_Unlocked.pdf")
    try:
        with open(output_file_name, 'wb') as out_file:
            pdf_writer.write(out_file)
            log_success(f'PDF unlocked - saved as {output_file_name}')
    except Exception as e:
        log_error(f'Failed to save {output_file_name}: {str(e)}')

# Initialize Rich console and progress bar
progress = Progress(console=console, transient=True)
task_id = progress.add_task('[cyan]Processing...', total=len(args.file))

# Loop over each file
for file_path in args.file:
    pdf_reader, pdf_file = process_pdf(file_path)
    if pdf_reader:
        pdf_writer = PyPDF2.PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        progress.update(task_id, advance=1)
        save_pdf(pdf_writer, file_path)
        pdf_file.close()

# Print output directory
log_info(f'Decrypted files saved in - {args.output_dir}')

# Finalize progress
progress.stop()
