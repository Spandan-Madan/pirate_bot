import io
import nltk.data
import re
import urllib2

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
	text = ""

	# Try various Gutenberg URLs
	try:
		url = 'http://www.gutenberg.org/files/{0}/{0}-0.txt'.format(book_id)
		text = urllib2.urlopen(url).read()
		if '</html>' in text: 
			raise Exception()
			print book_id, "html"
	except:
		try:
			url = 'http://www.gutenberg.org/cache/epub/{0}/pg{0}.txt'.format(book_id)
			text = urllib2.urlopen(url).read()
		except:
			pass # This is an audiobook

	# Trim extraneous header/footer text
	start_pattern = r'\*\*\*[^\*]*START[^\*]*GUTENBERG[^\*]*\*\*\*'
	end_pattern = r'\*\*\*[^\*]*END[^\*]*GUTENBERG[^\*]*\*\*\*'
	pattern = '{}(.*){}'.format(start_pattern, end_pattern)

	try:
		start = re.search(start_pattern, text).group()
		end = re.search(end_pattern, text).group()
		text = text.split(start)[1].split(end)[0]
	except:
		print book_id

	return text

def get_dialogue(text):
	# Text uses single quotation marks
	if text.count('\'') > text.count('"'):
		return []

	# Format text
	text = text.decode('utf-8', 'ignore')
	text = text.replace('\n', ' ')
	text = text.replace('\r', '')
	text = text.replace('\t', '')
	text = re.sub(r'\[[^\[]+\]', '', text)

	# Split text into sentences
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = tokenizer.tokenize(text)

	# Find text between quotes
	pattern = r'"([^"]*)"'
	quotes = [quote for sentence in sentences for quote in tokenizer.tokenize(' '.join(re.findall(pattern, sentence)))]
	return quotes


if __name__ == '__main__':
	pirate_book_ids = get_book_ids('pirate')
	pirate_dialogue = []

	# Create one large concatenated list of all dialogue
	for book_id in pirate_book_ids:
		text = get_book_text(book_id)
		pirate_dialogue += get_dialogue(text)
	print len(pirate_dialogue)

	# Write to text file
	text = '\n'.join(pirate_dialogue)
	with io.open('book_lines.txt', 'w', encoding='utf8') as text_file:
	    text_file.write(text)
