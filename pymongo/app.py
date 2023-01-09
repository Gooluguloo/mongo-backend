from flask import Flask,Blueprint, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
from flask_crontab import Crontab


app = Flask(__name__)
CORS(app)

client = MongoClient('localhost', 27017)

db = client.flask_db
pages = db.pages
wordIndex = db.wordIndex

keywords = db.keywords
webpages = db.webpages
pending_crawls = db.pending_crawls

from webpage.routes import module_webpages
app.register_blueprint(module_webpages)

crontab = Crontab(app)

from webpage.crawl import crawl_next_pending
crawl_next_pending()

@crontab.job(minute="*", hour="*")
def crawl_job():
    crawl_next_pending()
