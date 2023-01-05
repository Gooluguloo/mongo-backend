from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from webpage.models import WebPage
from bson.json_util import dumps, loads
import json

# from webpage.crawler import crawler
from app import  pages,wordIndex
from .crawler import crawler

module_webpages = Blueprint('module_webpages', __name__)

@module_webpages.route('/webpages/create', methods=['POST'])
def create_webpage():
    webpage = WebPage()
    webpage.url = request.form.get('url')
    webpage.title = request.form.get('title')
    webpage.description = request.form.get('description')
    if webpage.url == None or webpage.title == None or webpage.description == None:
        return "Insufficient data provided."
    pages.insert_one({'id': webpage.id, 'url': webpage.url, 'title': webpage.title, 'description' : webpage.description, 'created': webpage.created })
    return 'Webpage has been created successfully.'

@module_webpages.route('/webpages', methods=['GET'])
def list_webpages():

    results = json.loads(dumps(pages.find()))
    # print(results)
    return {
        'results': results
    }

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
