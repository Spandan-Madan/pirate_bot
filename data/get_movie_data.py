import nltk.data
import urllib2

# Load movie script URLs
with open('movie_urls.txt', 'r') as file:
	urls = [line.strip() for line in file.readlines()]

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

# Create one large concatenated list of all sentences
sentences = []
for url in urls:
	sentences += get_sentences(url)

# Write sentences to text file
text = '\n'.join(sentences)
with open("movie_lines.txt", "w") as text_file:
    text_file.write(text)
