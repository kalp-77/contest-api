import flask
import requests
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import json
import soup
from bs4 import BeautifulSoup


app = Flask(__name__)
CORS(app)
api = Api(app)

class Contest(Resource):
    def get(self,platform,username):
        user = soup.Data(username)
        return user.get_details(platform)

api.add_resource(Contest, "/api/<string:platform>/<string:username>")

if __name__ == '__main__':
    app.run()