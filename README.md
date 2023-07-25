# PDF_UTILS
This repository is meant to provide tools for working with PDFs. The following tools are included:
 - `pdf_unlock.py` - Removes password locks on PDFs provided you have the password to said PDF
 - `indexer.py` - Creates an alphabetically sorted word frequency based index from a PDF as the input file. Outputfile will be markdown for easy LaTeX MD -> PDF creation.

---
## pdf_unlock.py
```bash
python3 pdf_unlock.py $(cat <PASSWORD_FILE>) <PDF_FILE_TO_UNLOCK>
```

---
## indexer.py
```bash
python3 indexer.py --input <PDF_FILE_TO_INDEX> --output <MARKDOWN_OUTFILE> --book 1 --stopwords <STOP_WORD_LIST> 
```
