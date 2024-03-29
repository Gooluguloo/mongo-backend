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


def search(query, start=0, count=20):
    results = []

    _queries = process_context(query) + query.split('&')
    _keywords = []

    # Get keyword objects from queries
    # this performs fuzzy regex text search and grabs the first 25 matching keywords
    for q in _queries:
        for kw in keywords.find( { 'text': { '$regex': q } })[:25]:
            if kw and not kw in _keywords:
                _keywords.append(kw)
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

    total_count = len(results)
    start = int(start)
    count = int(count)

    if start >= len(results):
        results = results[0:20]
    elif start+count >= len(results):
        results = results[start:]
    else:
        results = results[start:start+count]

    # Return the result
    return {
        'total_count': total_count,
        'results': json.loads(dumps(results))
    }
