from flask import Blueprint, jsonify
# from app import pages
from .models import WebPage
from app import pages
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


count = 0

def extract_urls(url, depth=0):
    print("[Crawling] " + url)
    global count

    if count >= 20:
        return

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    record = {
        'url': url,
        'title': None,
        'description': None,
    }
    if soup.title is not None:
        title = soup.title.text
    else:
        title = ""
    description = soup.find("meta", property="og:description")
    if description == None:
        description = ""
    else:
        description = description.get("content")

    # existing = WebPage.query.filter(WebPage.url == url)
    count = pages.count_documents({"url" :url})

    if count > 0:
        print("[Duplicate] " + url)
        return

    webpage = WebPage()
    webpage.url = url
    webpage.title = title

    webpage.description = description
    # pages.insert_one({ 'url': webpage.url, 'title': webpage.title, 'description' : webpage.description, 'created': webpage.created.toString() })
    pages.insert_one({ 'url': webpage.url, 'title': webpage.title, 'description' : webpage.description,  })

    if depth > 0:
        return

    for link in soup.find_all('a'):
        path = link.get('href')
        if path and (path[0]==('/')):
            path = urljoin(url, path)
            extract_urls(path, depth+1)

    count += 1


def crawler(entry_url):
    results = extract_urls(entry_url)
    return results
