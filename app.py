import os
from flask import Flask, flash, redirect, render_template, request, session, abort, json
from random import randint
# import json

app = Flask(__name__)

@app.route("/")
def index():
    return "My App!"

@app.route("/hello/<string:name>/")
def hello(name):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "", "container8.json")
    data = json.load(open(json_url))

    quotes = data

    randomNumber = randint(0,len(quotes)-1)
    quote = quotes[randomNumber]

    return render_template(
        'test.html',**locals())

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80)
    app.run()
