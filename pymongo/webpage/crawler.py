from flask import Blueprint, jsonify
from app import pages, wordIndex
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import datetime
from bson.json_util import dumps

from .models import Webpage

count = 0


def extract_urls(url, depth=0):
    # print("[Crawling] " + url)
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

    # keyword = soup.find("meta", name="Keywords").string
    # paragraph = soup.find_all("p")
    # print(paragraph)
    context = ""
    for p in soup.find_all("p"):
        context += p.get_text()
        context += " "
    print(context)





    count = pages.count_documents({"url": url})

    # if count > 0:
    #     print("[Duplicate] " + url)
    #     return

    webpage = Webpage()
    webpage.url = url
    webpage.title = title
    webpage.keyword = context.split(" ")
    # print(webpage.keyword)
    webpage.description = description
    pages.insert_one({'url': webpage.url, 'title': webpage.title,
                     'description': webpage.description, 'keyword': webpage.keyword ,'createdAt': datetime.datetime.utcnow()})
    for word in webpage.keyword:
        thisword = wordIndex.find({'index': word})
        # urlArray = wordIndex.find({'index': )thisword.find({'url'})
        # print(urlArray)
        # print(dump_cursor(thisword))
        if dump_cursor(thisword) == "[]":
            print("[Add] added " + word + "into wordIndex")
            wordIndex.insert_one(
                {'index': word, 'count': description.split().count(word), 'occursAt' : [url]})
        else:
            print("[Update] update word" + word)
            wordIndex.update_one(
                {'index': word},
                {"$set":{'occursAt': [url]}})

    if depth > 0:
        return

    for link in soup.find_all('a'):
        path = link.get('href')
        if path and (path[0] == ('/')):
            path = urljoin(url, path)
            extract_urls(path, depth+1)

    count += 1


def crawler(entry_url):
    results = extract_urls(entry_url)
    return results
def dump_cursor(cursor):
    return dumps(list(cursor))
def parse_comma(word):
    return word.split(",")
