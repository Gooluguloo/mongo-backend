from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
import json

from app import webpages, keywords, pending_crawls

def list_webpages():
    results = json.loads(dumps(webpages.find()))
    return {
        'results': results
    }

def list_keywords():
    results = json.loads(dumps(keywords.find()))
    return {
        'results': results
    }

def list_pending_crawls():
    results = json.loads(dumps(pending_crawls.find()))
    return {
        'results': results
    }
