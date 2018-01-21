import os
import container_search
from flask import Flask, flash, redirect, render_template, request, session, abort, json
from random import randint


my_c = container_search.ContainerSearch()
data = my_c.data
# c = my_c.c
dimensions = my_c.dimensions


from flask import Flask
from flask import request
from flask import render_template




app = Flask(__name__)


# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('results.html', name=name)


@app.route("/")
# def my_form():
#     return render_template("test.html")

def index():

    randomNumber = randint(0,len(data)-1)
    c = data[randomNumber]
    # c = data[0]

    if len(c['dimensions'])>0:

        r = randint(0,len(c['dimensions'])-1)

    return render_template(
        'test.html',**locals())

@app.route('/', methods=['POST'])
def my_form_post():

    l = request.form['text']
    w = request.form['text2']
    h = request.form['text3']
    values=[float(l),float(w),float(h)]
    pf = my_c.the_perfect_fit_values(values,2.)
    possibles = pf[0][3]
    possibles_text = 'There are '+str(len(possibles))+ ' containers that are within '+ str(pf[1])+ '\" of your space: '+ str(values[0])+'" x '+ str(values[1])+'" x '+ str(values[2])+'"'


    return render_template('results.html',**locals())

    # return render_template('results.html', name=possibles_text)

    # return possibles_text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    # app.run()
