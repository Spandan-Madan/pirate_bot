import argparse
import nltk.data
import re
import urllib2

def query_poem_urls_for_tag(tag):
    pattern = r'<a href="/poem/([^"]*)"'
    poem_urls = set()
    page_number = 1

    while True:
        query_url = 'https://www.hellopoetry.com/search/poems/?q={}&page={}'.format(tag, page_number)
        text = urllib2.urlopen(query_url).read()
        paths = re.findall(pattern, text)
        if len(paths) > 0:
            poem_urls.update(['https://www.hellopoetry.com/poem/{}'.format(path) for path in paths])
        else:
            break
        page_number += 1

    return poem_urls

def query_poem_urls(tags):
    poem_urls = set()
    for tag in tags:
        poem_urls.update(query_poem_urls_for_tag(tag))
    return poem_urls

def get_all_pirate_poem_urls():
    # Get set of pirate poem URLs
    tags = ['pirate', 'pirates', 'shipwreck', 'shipwrecks']
    urls = query_poem_urls(tags)
    return urls

def get_lines(url):
    # Get HTML
    response = urllib2.urlopen(url)
    html = response.read()

    # Parse HTML into plain text
    pattern = r'<div class="poem-part continue-reading poem-body wordwrap">([\s\S]*?)</div>'
    line_text = re.search(pattern, html).group(1).strip()
    line_text = re.sub(r'<[^<>]+>', '', line_text)
    line_text = line_text.decode('ascii', errors='ignore').encode()
    line_text = line_text.replace('&nbsp;', '')

    # Parse text into list of lines
    lines = line_text.split('<br>')
    lines = [line.strip() for line in filter(None, lines)]
    return lines

def get_all_lines(urls):
    return [line for url in urls for line in get_lines(url)]


if __name__ == '__main__':
    urls = get_all_pirate_poem_urls()
    lines = get_all_lines(urls)
    text = '\n'.join(lines)
    print len(lines)

    # Write to text file
    with open('poem_lines.txt', 'w') as text_file:
        text_file.write(text)
