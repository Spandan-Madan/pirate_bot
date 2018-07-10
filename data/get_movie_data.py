import argparse
import nltk.data
import re
import urllib2

def load_movie_urls(filename='movie_urls.txt'):
    with open(filename, 'r') as file:
        urls = set([line.strip() for line in file.readlines()])
    return urls

def query_movie_urls_for_keyword(keyword):
    pattern = r'<a href="([^"]*)" class="script-list-item"'
    movie_urls = set()
    page_number = 1

    while True:
        query_url = 'https://www.springfieldspringfield.co.uk/movie_scripts.php?search={}&page={}'.format(keyword, page_number)
        text = urllib2.urlopen(query_url).read()
        paths = re.findall(pattern, text)
        if len(paths) > 0:
            movie_urls.update(['https://www.springfieldspringfield.co.uk{}'.format(path) for path in paths])
        else:
            break
        page_number += 1

    return movie_urls

def query_movie_urls(keywords):
    movie_urls = set()
    for keyword in keywords:
        movie_urls.update(query_movie_urls_for_keyword(keyword))
    return movie_urls

def get_all_pirate_movie_urls():
    # Get set of pirate movie URLs
    keywords = ['pirate', 'pirates', 'treasure', 'ship', 'buccaneer', 'captain', 'sea', 'gold',
        'deep', 'ocean', 'jaws', 'blackbeard', 'yellowbeard', 'pan', 'viking', 'vikings', 'sails',
        'corsair']
    urls = query_movie_urls(keywords)
    urls.update(load_movie_urls())

    # Remove any banned urls
    banned_urls = load_movie_urls('banned_movie_urls.txt')
    urls -= banned_urls
    return urls

def get_sentences(url):
    # Get HTML
    response = urllib2.urlopen(url)
    html = response.read()

    # Parse HTML into plain text
    text = html.split('<div class="scrolling-script-container">')[1].split('</div>')[0]
    text = text.replace("<br>", "")
    text = text.replace(" - ", " ")
    text = text.replace("\'", "'")
    text = text.lstrip()

    # Parse text into a list of sentences
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text)

    title = re.search(r'<title>([^"]+) Movie Script', html).group(1)
    return [(sentence, title) for sentence in sentences]

def get_all_sentences(urls):
    return [(sentence, title) for url in urls for (sentence, title) in get_sentences(url)]

def get_all_sentence_pairs(urls):
    sentence_pairs = []
    for url in urls:
        sentences = get_sentences(url)
        sentence_pairs += zip(sentences, sentences[1:])
    return sentence_pairs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pairs', action='store_true')
    args = parser.parse_args()
    urls = get_all_pirate_movie_urls()
    text = ""

    if args.pairs:
        sentence_pairs = get_all_sentence_pairs(urls)

        # Combine Q/A pairs in tab-delimted format
        text = 'line\tresponse\n'
        for line, response in sentence_pairs:
            text += '{}\t{}\n'.format(line, response)
    else:
        sentences = get_all_sentences(urls)
        text = ''
        for sentence, title in sentences:
            text += '{}\t{}\n'.format(sentence, title)

    # Write to text file
    filename = 'movie_line_pairs.txt' if args.pairs else 'movie_lines.txt'
    with open(filename, 'w') as text_file:
        text_file.write(text)
