# PDF_UTILS
This repository is meant to provide tools for working with PDFs. The following tools are included:
 - `pdf_unlock.py` - Removes password locks on PDFs provided you have the password to said PDF
 - `indexer.py` - Creates an alphabetically sorted word frequency based index from a PDF as the input file. Outputfile will be markdown for easy LaTeX MD -> PDF creation.

---
## Setup
It is recommended to install tool dependencies within a virtual environment. Setup for that is below:
```bash
[-] python3 -m venv bin/activate <ENVIRONMENT_NAME>

[-] source <ENVIRONMENT_NAME>/bin/activate

[-] python3 -m pip install -r requirements.txt
```

---
## pdf_unlock.py

### pdf_unlock.py - Help Text
```bash
[-] python3 pdf_unlock_0.02.py -h                                                              

		usage: pdf_unlock_0.02.py [-h] [--pass_file password_file] [--file files [files ...]]
		
		Decrypt password-protected PDFs.
		
		options:
		  -h, --help            show this help message and exit
		  --pass_file password_file, -p password_file
		                        the file containing the password for the PDFs
		  --file files [files ...], -f files [files ...]
		                        the paths to the PDFs
```

### pdf_unlock.py - Examples
```bash
# For a Single File
python3 pdf_unlock_0.02.py --pass_file password.txt --file <FILE1>

# For Multiple Files
python3 pdf_unlock_0.02.py --pass_file password.txt --file <FILE1> <FILE2> <FILE__N__>
```

---
## indexer.py

### indexer.py - Help Text
```bash
[-] python3 indexer.py -h

		usage: indexer.py [-h] [--input INPUT [INPUT ...]] [--output OUTPUT] [--book BOOK [BOOK ...]]
		                       [--stopwords STOPWORDS] [--commonwords COMMONWORDS] [--exportfreq] [--freqfile FREQFILE]
		                       [--freqlimit FREQLIMIT]
		
		Generate an index from a PDF file.
		
		options:
		  -h, --help            show this help message and exit
		  --input INPUT [INPUT ...], -i INPUT [INPUT ...]
		                        Your input PDF file(s)
		  --output OUTPUT, -o OUTPUT
		                        Your output markdown file
		  --book BOOK [BOOK ...], -b BOOK [BOOK ...]
		                        Your book number(s)
		  --stopwords STOPWORDS, -s STOPWORDS
		                        Your custom stopwords
		  --commonwords COMMONWORDS, -c COMMONWORDS
		                        Your common words
		  --exportfreq, -e      Export word frequencies
		  --freqfile FREQFILE, -f FREQFILE
		                        The file to export the frequencies to
		  --freqlimit FREQLIMIT, -l FREQLIMIT
		                        The frequency limit for words to be included
```

### indexer.py - Examples
```bash
# Index Single File
[-] python3 indexer.py --input "FILE1" --output <OUTFILE> --book "1" -s <CUSTOM_FINE_GRAINED_WORDLIST> -c <COMMON_STOP_WORDS>

# Index Multiple Files
[-] python3 indexer.py --input "FILE1" "FILE2" "FILE3" "FILE4" "FILE5" "FILE__N__" --output <OUTFILE> --book "1" "2" "3" "4" "5" "W1" -s <CUSTOM_FINE_GRAINED_WORDLIST> -c <COMMON_STOP_WORDS>

```
