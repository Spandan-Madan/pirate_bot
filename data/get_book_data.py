
import io
import nltk.data
import re
import urllib2

from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_metadata

def query_book_results(query_url):
    # Parse the HTML from the query to obtain a list of book ids
    pattern = '<li class="booklink">\n<a class="link" href="/ebooks/([0-9]+)"'
    html = urllib2.urlopen(query_url).read()
    book_ids = re.findall(pattern, html)
    return book_ids

def get_book_ids(query):
    book_ids = []
    start_index = 1

    # Crawl through query results pages
    while True:
        query_url = 'http://www.gutenberg.org/ebooks/search/?start_index={}&query={}+l.en'.format(start_index, query)
        results = query_book_results(query_url)
        if len(results) > 0:
            book_ids += results
            start_index += 25
        else:
            break

    return book_ids

def get_book_text(book_id):
    return strip_headers(load_etext(int(book_id))).strip()

def get_book_title(book_id):
    return get_metadata('title', int(book_id))

def get_dialogue(text, title):
    # Text uses single quotation marks
    if text.count('\'') > text.count('"'):
        return []

    # Format text
    # text = text.encode('utf-8', 'ignore')
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    text = text.replace('\t', '')
    text = re.sub(r'\[[^\[]+\]', '', text)

    # Split text into sentences
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text)

    # Find text between quotes
    pattern = r'"([^"]*)"'
    quotes = [(quote, title) for sentence in sentences for quote in tokenizer.tokenize(' '.join(re.findall(pattern, sentence)))]
    return quotes


if __name__ == '__main__':
    pirate_book_ids = get_book_ids('pirate')
    pirate_dialogue = []

    # Create one large concatenated list of all dialogue
    for book_id in pirate_book_ids:
        try:
            title = get_book_title(book_id)
            text = get_book_text(book_id)
        except:
            pass
        pirate_dialogue += get_dialogue(text, title)

    # Write to text file
    text = ''
    for quote, title in pirate_dialogue:
        text += '{}\t{}\n'.format(quote.encode('utf-8', 'ignore'), title)
    with open('book_lines.txt', 'w') as text_file:
        text_file.write(text)
