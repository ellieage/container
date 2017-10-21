import os
from flask import Flask, flash, redirect, render_template, request, session, abort, json
from random import randint
# import json

app = Flask(__name__)

@app.route("/")
def index():
    # return "My App!"

# @app.route("/hello/<string:name>/")
# def hello(name):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "", "container.json")
    data = json.load(open(json_url))

    randomNumber = randint(0,len(data)-1)
    c = data[randomNumber]
    # c = data[0]

    r = randint(0,len(c['dimensions'])-1)

    return render_template(
        'test.html',**locals())

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80)
    app.run()
