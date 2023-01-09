from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
import json

# from webpage.crawler import crawler
from app import pages, webpages, keywords
from .crawl import crawl_webpage, crawl_next_pending
from .crud import list_keywords, list_webpages, list_pending_crawls
from .search import search

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

@module_webpages.route('/pending', methods=['GET'])
def _list_pending_crawls():
    return list_pending_crawls()
