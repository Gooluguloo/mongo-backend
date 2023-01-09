from flask import Blueprint, jsonify
from app import webpages, keywords, pending_crawls
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import datetime
from bson.json_util import dumps
from urllib.parse import urljoin
import validators

from .textprocess import process_context


def enqueue_urls(base_url, urls):
    for _url in urls:
        url = urljoin(base_url, _url)

        # Skip if url is invalid, or webpage already exists, or url already in queue
        if not validators.url(url):
            continue
        if webpages.count_documents({ 'url': url }) > 0:
            continue
        if pending_crawls.count_documents({ 'url': url }) > 0:
            continue
            
        pending_crawls.insert_one({
            'url': url,
            'added': datetime.datetime.now()
        })


def index_keywords(webpage, words):
    # An empty keyword list
    _keywords = []

    # Iterate every word
    for key in words:
        # The frequency of the current word in this webpage
        frequency = words[key]

        # If word is already recorded, update
        if keywords.find_one( { 'text': key }):
            keywords.update_one(
                { 'text': key },
                {
                    # Add frequency to the total frequency of the word
                    '$inc': {
                        'total_frequency': frequency,
                    },
                    # Add to the entries list (which webpage, and the frequency in it)
                    '$push': {
                        'entries': {
                            'webpage_id': webpage.inserted_id,
                            'freq': frequency,
                        }
                    },
                },
            )

        # If not yet recorded, create record
        else:
            keyword = keywords.insert_one({
                'text': key,
                'total_frequency': words[key],
                'entries': [{
                    'webpage_id': webpage.inserted_id,
                    'freq': frequency,
                }]
            })


def index_webpage(url, title, description):
    webpage = webpages.insert_one({
        'url': url,
        'title': title,
        'description': description
    })
    return webpage


# Process a crawled HTML context
def process_webpage(url, html):
    if not validators.url(url):
        return
    if webpages.find_one( { 'url': url } ):
        return

    soup = BeautifulSoup(html, 'html.parser')

    # Extract webpage information
    title = soup.title.text if soup.title else ""
    _description = soup.find('meta', property="og:description")
    description = _description.get('content') if _description else ""

    # Extract main context and tokenize the words
    context = soup.get_text()
    # for tag in TAGS_TO_EXTRACT:
    #     for p in soup.find_all(tag):
    #         context += f'{ p.get_text() } '
    #         context += f'{ p.get_text() } '

    # Add description keywords to main context as well
    _desc_keywords = process_context(description)
    context += ' '.join(_desc_keywords)

    # Perform lemmatization and tokenization
    _words = process_context(context)

    # Calculate the frequency of each word
    words = {}
    for w in _words:
        if w in words:
            words[w] += 1
        else:
            words[w] = 1

    # Index the webpage
    webpage = index_webpage(url, title, description)

    # Index the words
    index_keywords(webpage, words)

    urls = []
    for a in soup.find_all('a', href=True):
        urls.append(a['href'])
    enqueue_urls(url, urls)



# Entry point to crawl an url
def crawl_webpage(url):
    # Preprocess the url
    url = url.replace("%WANG", "/")
    if not url.startswith('http'):
        url = f'https://{url}'
    if not validators.url(url):
        return

    # Skip if the page has already been crawled
    if webpages.find_one( { 'url': url } ):
        return 'Webpage has already been crawled. Skipping...'

    html = requests.get(url).text
    process_webpage(url, html)

    return 'Webpage crawl success.'


# Crawl the first item in the pending queue
def crawl_next_pending():
    if pending_crawls.find():
        return
    item = pending_crawls.find({})[0]
    crawl_webpage(item['url'])
    pending_crawls.delete_one({ '_id': item['_id'] })
