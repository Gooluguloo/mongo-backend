from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from webpage.models import Webpage
from bson.json_util import dumps, loads
import json

# from webpage.crawler import crawler
from app import pages, webpages, keywords
from .crawl import crawl_webpage
from .crud import list_keywords, list_webpages
from .search import search

module_webpages = Blueprint('module_webpages', __name__)

@module_webpages.route('/search/<query>', methods=['GET'])
def _search(query:str):
    return search(query)

@module_webpages.route('/webpages/process/<url>', methods=['GET'])
def _crawl(url:str):
    return crawl_webpage(url)

@module_webpages.route('/webpages', methods=['GET'])
def _list_webpages():
    return list_webpages()

@module_webpages.route('/keywords', methods=['GET'])
def _list_keywords():
    return list_keywords()
