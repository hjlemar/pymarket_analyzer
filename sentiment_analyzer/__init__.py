from flask import Flask, jsonify
from flask_restx import Api
from werkzeug import cached_property


app = Flask(__name__)
app.config.from_object('config')
api = Api(app)


import sentiment_analyzer.views

