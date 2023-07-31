import argparse
import fitz
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter
from tqdm import tqdm
import os
import csv

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def valid_word(word):
    if len(word.split()) > 1:  # If it's a bigram or trigram, it's okay to have spaces
        # Word should only contain letters, numbers, hyphens, or spaces, and should not start or end with a digit
        if re.match(r'^\d', word) or re.search(r'\d$', word) or not re.match(r'^[a-zA-Z0-9- ]*$', word): 
            return False
        else:
            return True
    else:  # If it's a unigram, it shouldn't have any non-alphanumeric or non-hyphen characters, or start with a digit
        if re.match(r'^\d', word) or not re.match(r'^[a-zA-Z0-9-]*$', word): 
            return False
        else:
            return True

def convert_to_markdown(word_pages: dict, freq_limit: int = 10) -> str:
    markdown_list = []

    sorted_word_pages = {word: pages for word, pages in word_pages.items() if sum(len(v) for v in pages.values()) <= freq_limit}
    sorted_word_pages = dict(sorted(sorted_word_pages.items(), key=lambda item: item[0].lower()))

    current_section = None

    for word, book_pages in sorted_word_pages.items():
        if not valid_word(word): 
            continue

        # Get the first character of the word
        first_char = word[0].upper()

        # If the first character is not a letter, use a special section
        if not first_char.isalpha():
            first_char = "Numbers & Symbols"

        # If the section has changed, add a header
        if first_char != current_section:
            markdown_list.append(f"# {first_char}")
            current_section = first_char

        page_list = []
        for book_number, pages in book_pages.items():
            page_list.extend([f"{book_number}.{p}" for p in pages])

        # Remove duplicate page entries
        page_list = list(set(page_list))

        # Sort the page list
        page_list.sort()

        markdown_list.append(f'- **{word}**: {", ".join(page_list)}')

    markdown_text = '\n'.join(markdown_list)
    return markdown_text

def process_pdf(file, book_number, custom_stopwords, freq_limit: int = 10):
    doc = fitz.open(file)
    text = ""
    words_pages = {}
    word_freq = Counter()

    for i in tqdm(range(len(doc)), desc=f"Processing {file}", ncols=100):
        page = doc.load_page(i)
        text = page.get_text("text")
        words = word_tokenize(text)
        words = [word for word in words if not word.lower() in custom_stopwords]
        for word in words:
            if word not in words_pages:
                words_pages[word] = {book_number: []}
            elif book_number not in words_pages[word]:
                words_pages[word][book_number] = []
            words_pages[word][book_number].append(i+1-2)

        # Generate bi-grams, tri-grams, and quad-grams without overlap
        bigrams = [' '.join(bg) for bg in zip(words, words[1:])]
        trigrams = [' '.join(tg) for tg in zip(words, words[1:], words[2:])]
        quadgrams = [' '.join(qg) for qg in zip(words, words[1:], words[2:], words[3:])]

        # Combine bigrams, trigrams, and quadgrams into one list
        ngrams_list = bigrams + trigrams + quadgrams

        for ng in ngrams_list:
            # Check if the first word of the n-gram is a stopword
            first_word = ng.split()[0].lower()
            if first_word in custom_stopwords:
                continue
            if ng not in words_pages:
                words_pages[ng] = {book_number: []}
            elif book_number not in words_pages[ng]:
                words_pages[ng][book_number] = []
            words_pages[ng][book_number].append(i+1-2)

    word_pages = {word: pages for word, pages in words_pages.items() if word_freq[word] <= freq_limit}

    return words_pages, word_freq

def get_custom_stopwords(stopwords_input):
    if os.path.exists(stopwords_input):  
        with open(stopwords_input, 'r') as f:
            stopwords_text = f.read()
        stopwords_list = re.split(',|\n', stopwords_text)  # split by comma or newline
    else:
        stopwords_list = stopwords_input.split(',')
    stopwords_list = [word.strip() for word in tqdm(stopwords_list, desc=f"Loading stopwords from {stopwords_input}", ncols=100)]  # remove any leading/trailing whitespace
    return set(word.lower() for word in stopwords_list)

def export_word_frequency(word_freq, freq_file):
    with open(freq_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Word', 'Frequency'])
        for word, freq in word_freq.items():
            writer.writerow([word, freq])

parser = argparse.ArgumentParser(description='Generate an index from a PDF file.')
parser.add_argument('--input', '-i', nargs='+', help='Your input PDF file(s)')
parser.add_argument('--output', '-o', help='Your output markdown file', default='')
parser.add_argument('--book', '-b', nargs='+', help='Your book number(s)', default=[])
parser.add_argument('--stopwords', '-s', help='Your custom stopwords', default='')
parser.add_argument('--commonwords', '-c', help='Your common words', default='')
parser.add_argument('--exportfreq', '-e', action='store_true', help='Export word frequencies')
parser.add_argument('--freqfile', '-f', help='The file to export the frequencies to', default='frequencies.csv')
parser.add_argument('--freqlimit', '-l', help='The frequency limit for words to be included', type=int, default=10)
args = parser.parse_args()

custom_stopwords = get_custom_stopwords(args.stopwords)
common_words = get_custom_stopwords(args.commonwords)
custom_stopwords = custom_stopwords.union(common_words)

if args.input is None or len(args.input) != len(args.book) or (args.output is None and not args.exportfreq):
    print("You must provide equal numbers of input files and book numbers, and either an output file or the --exportfreq flag.")
else:
    words_pages = {}
    word_freq = Counter()

    for i, input_file in enumerate(args.input):  # process each PDF file
        words_pages_temp, word_freq_temp = process_pdf(input_file, args.book[i], custom_stopwords, args.freqlimit)
        for word, books in words_pages_temp.items():
            if word not in words_pages:
                words_pages[word] = books
            else:
                words_pages[word].update(books)
        word_freq += word_freq_temp  # Merge frequencies from different PDFs
        if args.exportfreq:
            export_word_frequency(word_freq_temp, f"{args.freqfile}_{args.book[i]}")  # save frequencies with book number

    markdown_text = convert_to_markdown(words_pages, args.freqlimit)

    if args.exportfreq:
        export_word_frequency(word_freq, args.freqfile)  # save combined frequencies

    print("Attempting to write to: ", os.path.abspath(args.output))
    try:
        with open(args.output, 'w') as md_file:
            md_file.write(markdown_text)
        print("Successfully written to: ", args.output)
    except Exception as e:
        print(f"Error writing to file: {e}")
