from flask import Flask,Blueprint, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

client = MongoClient('localhost', 27017)

db = client.flask_db
pages = db.pages


from webpage.routes import module_webpages
app.register_blueprint(module_webpages)
