import logging
import operator
import tempfile
import json
from urllib.request import urlopen

import requests

from flask import Flask, jsonify, redirect, url_for, request, Response
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)


# Some useful base constants (for URLS and such)
database = "localhost:27017"
logging.basicConfig(filename='prod.log', level=logging.DEBUG)

# The database instance
client = MongoClient(database)
db = client.production

# ---------------------------------
# RUNNERS, RUNTIME AND ROUTES BELOW
# ----------------------------------


@app.route("/api/post_request", methods=['POST'])
def take_input():
    # Sample POST:
    # {hospital: "HOSPITAL HERE", type: "telephone", content: "TESTING FINAL"}
    content = request.get_json(force=True)
    submission = {
        "hospital": content['hospital'],
        "type": content['type'],
        "content": content['content']
    }
    db.mvp.insert_one(submission)
    print("Recieved post request and inserted into the DB.")
    resp = Response(response="true", status=200,  mimetype="application/json")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/api/all_data")
def send_response():
    content = json.dumps(list(db.mvp.find({})), default=json_util.default)
    resp = resp = Response(
        response=content, status=200,  mimetype="application/json")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/")
def home():
    resp = Response("")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return redirect(url_for('static', filename='index.html'))


# -----------
# LET IT RUN!
# -----------
if __name__ == "__main__":
    print(" ")
    print("RRRRRR  UU   UU NN   NN NN   NN IIIII NN   NN   GGGG ")
    print("RR   RR UU   UU NNN  NN NNN  NN  III  NNN  NN  GG  GG ")
    print("RRRRRR  UU   UU NN N NN NN N NN  III  NN N NN GG      ")
    print("RR  RR  UU   UU NN  NNN NN  NNN  III  NN  NNN GG   GG ")
    print("RR   RR  UUUUU  NN   NN NN   NN IIIII NN   NN  GGGGGG ")
    print(" ")
    app.run(host='0.0.0.0', port=3000)
