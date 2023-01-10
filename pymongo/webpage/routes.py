from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
import json

# from webpage.crawler import crawler
<<<<<<< HEAD
from app import pages, webpages, keywords
from .crawl import crawl_webpage, crawl_next_pending
from .crud import list_keywords, list_webpages, list_pending_crawls
from .search import search
=======
from app import  pages,wordIndex
from .crawler import crawler
>>>>>>> d69702601de23cf2c29b0c417a7d5a225346aa1b

module_webpages = Blueprint('module_webpages', __name__)

@module_webpages.route('/search/<query>', methods=['GET'])
def _search(query:str):
    # 0: Search query; 1: Start index; 2: Retrieve count
    params = query.split('%SPL')

    if len(params) == 3:
        return search(params[0], params[1], params[2])
    elif len(params) == 2:
        return search(params[0], params[1])
    else:
        return search(params[0])


@module_webpages.route('/crawl/<url>', methods=['GET'])
def _crawl(url:str):
    return crawl_webpage(url)

@module_webpages.route('/crawl-next', methods=['GET'])
def _crawl_next_pending():
    return crawl_next_pending()

@module_webpages.route('/webpages', methods=['GET'])
def _list_webpages():
    return list_webpages()

@module_webpages.route('/keywords', methods=['GET'])
def _list_keywords():
    return list_keywords()

<<<<<<< HEAD
@module_webpages.route('/pending', methods=['GET'])
def _list_pending_crawls():
    return list_pending_crawls()
=======
@module_webpages.route(r'/webpages/crawl/<sitelink>', methods=['GET'])
def crawl(sitelink:str):
    sitelink = sitelink.replace('%WANG', "/")
    print(sitelink)
    # try:
    crawler(sitelink)
    return {
        'result': 'Crawling complete.'
    }

    # except:
    #     return {
    #         'result': 'Crawling failed.'
    #     }

@module_webpages.route(r'/webpages/search/<querystr>', methods=['GET'])
def search(querystr: str):
    output:json = []
    for word in querystr.split("+"):
        result = wordIndex.find({'index': word })
        output =  output + json.loads(dumps(result))
    return output





def dump_cursor(cursor):
    return dumps(list(cursor))
>>>>>>> d69702601de23cf2c29b0c417a7d5a225346aa1b
