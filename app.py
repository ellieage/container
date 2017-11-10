import os
import container_search
from flask import Flask, flash, redirect, render_template, request, session, abort, json
from random import randint
# import json

my_c = container_search.ContainerSearch()
data = my_c.data
c = my_c.c
dimensions = my_c.dimensions


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
    # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    # json_url = os.path.join(SITE_ROOT, "", "data_cleaned.json")
    # data = json.load(open(json_url))
    # c_url = os.path.join(SITE_ROOT, "", "data_c.json")
    # c = json.load(open(c_url))
    # c_url = os.path.join(SITE_ROOT, "", "data_c.json")
    # c = json.load(open(c_url))
    # dim_url = os.path.join(SITE_ROOT, "", "data_dim.json")
    # dimensions = json.load(open(dim_url))



    randomNumber = randint(0,len(data)-1)
    c = data[randomNumber]
    # c = data[0]

    if len(c['dimensions'])>0:

        r = randint(0,len(c['dimensions'])-1)

    return render_template(
        'test.html',**locals())

@app.route('/', methods=['POST'])
def my_form_post():
    # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    # json_url = os.path.join(SITE_ROOT, "", "data_cleaned.json")
    # data = json.load(open(json_url))
    # c_url = os.path.join(SITE_ROOT, "", "data_c.json")
    # c = json.load(open(c_url))
    # c_url = os.path.join(SITE_ROOT, "", "data_c.json")
    # c = json.load(open(c_url))
    # dim_url = os.path.join(SITE_ROOT, "", "data_dim.json")
    # dimensions = json.load(open(dim_url))

    # my_c = container_search.ContainerSearch(data, c, dimensions)
    l = str(request.form['text'])
    w = str(request.form['text2'])
    h = str(request.form['text3'])
    values=[float(l),float(w),float(h)]
    pf = my_c.the_perfect_fit_values(values,2.)
    possibles = pf[3]
    possibles_text = 'There are '+str(len(possibles))+ ' containers that will fit your space: '+ str(values)+'<br>'
    # print('')
    for c in possibles:
        possibles_text+='<br> <a href='+str(c[0]['url'])+'>'+str(c[0]['title']) + ", '"+str(c[0]['category'])+ "'" +'<br>' +str(c[0]['dimensions'][c[1]])+'<br>'  +'<img src="'+str(c[0]['image'][0])+'/">' +'</a>' #+str(c[0]['price'][c[1]])+'<br>'


    # text = request.form['text']
    # processed_text = text.upper()
    return possibles_text

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80)
    app.run()
