import argparse
import nltk.data
import re
import urllib2

def load_saved_movie_urls(filename='movie_urls.txt'):
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
    keywords = ['pirate', 'pirates', 'treasure', 'ship', 'buccaneer', 'captain', 'sea', 'gold',
        'deep', 'ocean', 'jaws', 'blackbeard', 'yellowbeard', 'pan', 'viking', 'vikings', 'sails',
        'corsair']
    urls = query_movie_urls(keywords)
    urls.update(load_saved_movie_urls())
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
    return sentences

def filter(text, filter_words=None):
    if filter_words == None:
        with open('filter_list.txt', 'r') as filter_file:
            filter_words = set(filter_file.readlines())
    return not any(word.lower() in text.lower() for word in filter_words)

def get_all_sentences(urls):
    return [sentence for url in urls for sentence in get_sentences(url) if filter(sentence)]

def get_all_sentence_pairs(urls):
    sentence_pairs = []
    for url in urls:
        sentences = get_sentences(url)
        sentence_pairs += zip(sentences, sentences[1:])

    # Remove pairs containing filter words
    sentence_pairs = [(line, response) for (line, response) in sentence_pairs if filter(line) and filter(response)]
    return sentence_pairs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pairs', action='store_true')
    args = parser.parse_args()
    urls = get_all_pirate_movie_urls()
    text = ""
        
    if args.pairs:
        print "pairs"
        sentence_pairs = get_all_sentence_pairs(urls)

        # Combine Q/A pairs in tab-delimted format
        text = 'line\tresponse\n'
        for line, response in sentence_pairs:
            text += '{}\t{}\n'.format(line, response)
    else:
        print "not pairs"
        sentences = get_all_sentences(urls)
        text = '\n'.join(sentences)

    # Write to text file
    filename = 'movie_line_pairs.txt' if args.pairs else 'movie_lines.txt'
    with open(filename, 'w') as text_file:
        text_file.write(text)
