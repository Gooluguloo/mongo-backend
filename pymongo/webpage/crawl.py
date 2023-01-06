from flask import Blueprint, jsonify
from app import webpages, keywords
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import datetime
from bson.json_util import dumps

from .models import Webpage, Keyword
from .textprocess import process_context


# TAGS_TO_EXTRACT = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span', 'a', 'code', 'blockquote']


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



# Entry point to crawl an url
def crawl_webpage(url):
    # Preprocess the url
    url = url.replace("%WANG", "/")
    if not url.startswith('http'):
        url = f'https://{url}'

    # Skip if the page has already been crawled
    if webpages.find_one( { 'url': url } ):
        return 'Webpage has already been crawled. Skipping...'

    html = requests.get(url).text
    process_webpage(url, html)

    return 'Webpage crawl success.'
