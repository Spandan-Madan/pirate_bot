from selenium import webdriver
driver = webdriver.PhantomJS()
query = 'pirates'

NUM_GOOGLE_PAGES = 10
NUM_BOOK_PAGES_TO_READ = 200

for i in range(NUM_GOOGLE_PAGES):
	driver.get('https://www.google.com/search?q=%s&tbm=bks&source=lnt&tbs=bkv:r&start=%s'%(query,i*10))
	all_links = driver.find_elements_by_tag_name('a')

# can get it to read more books by scrolling the page when it's 
book_ids = []
for link in all_links:
	url = link.get_attribute('href')
	if url == None:
		continue
	if url.startswith("https://books.google.com/books?id="):
		book_id = url.split('id=')[1].split('&print')[0]
		book_ids.append(book_id)


print('Reading %s books'%len(book_ids))

all_text = []
for book_id in book_ids:
	book_text = []
	for i in range(1,int(NUM_BOOK_PAGES_TO_READ/5)+1,5):
		textbook_url = 'https://books.google.com/books?id=' + book_id + '&pg=PA%s&focus=viewport&output=text'%i
		driver.get(textbook_url)
		all_p = driver.find_elements_by_tag_name('p')
		for p in all_p:
			book_text.append(p.text)
	all_text.extend(book_text)

print('I read %s lines'%len(all_text))

for line in all_text:
	print(line)