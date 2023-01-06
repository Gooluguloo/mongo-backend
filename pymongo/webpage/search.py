from flask import Blueprint, jsonify
from app import webpages, keywords
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import datetime
from bson.json_util import dumps
from .textprocess import process_context
import json

def partition(arr, low, high):
    pivot = arr[high]['total_frequency']
    i = low-1
    for j in range(low, high):
        if arr[j]['total_frequency'] < pivot:
            i += 1
            arr[j], arr[i] = arr[i], arr[j]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1

def quicksort(keywords, low, high):
    if low < high:
        pivot = partition(keywords, low, high)
        quicksort(keywords, low, pivot-1)
        quicksort(keywords, pivot+1, high)


def search(query):
    results = []

    _queries = process_context(query) + query.split('&')
    _keywords = []

    # Get keyword objects from queries
    for q in _queries:
        keyword = keywords.find_one( { 'text': q } )
        if keyword:
            _keywords.append(keyword)
    # Sort the found keywords based on their total frequencies (low to high)
    quicksort(_keywords, 0, len(_keywords)-1)

    # Iterate all the found keywords
    for kw in _keywords:
        # Iterate the entries of each keyword
        for entry in kw['entries']:
            # Find the corresponding webpage for the entry
            webpage = webpages.find_one( { '_id': entry['webpage_id'] } )
            # If the webpage has not been included, include it
            if not webpage in results:
                results.append(webpage)

    # Return the result
    return json.loads(dumps(results))
