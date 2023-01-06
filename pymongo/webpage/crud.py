from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
from webpage.models import Webpage
from bson.json_util import dumps, loads
import json

from app import webpages, keywords

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
