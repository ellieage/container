import os
from flask import Flask, flash, redirect, render_template, request, session, abort, json
from random import randint
# import json

from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)

@app.route("/")
# def my_form():
#     return render_template("test.html")

def index():
    # return "My App!"

# @app.route("/hello/<string:name>/")
# def hello(name):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "", "data_cleaned.json")
    data = json.load(open(json_url))

    randomNumber = randint(0,len(data)-1)
    c = data[randomNumber]
    # c = data[0]

    if len(c['dimensions'])>0:

        r = randint(0,len(c['dimensions'])-1)
    
    return render_template(
        'test.html',**locals())

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    processed_text = text.upper()
    return processed_text

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80)
    app.run()
