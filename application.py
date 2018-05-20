import os
import container_search
from flask import Flask, flash, redirect, render_template, request, session, abort, json
from random import randint
from fractions import Fraction

from flask_bootstrap import Bootstrap

my_c = container_search.ContainerSearch()
data = my_c.data
# c = my_c.c
dimensions = my_c.dimensions


from flask import Flask
from flask import request
from flask import render_template




application = app = Flask(__name__)

bootstrap = Bootstrap(app)

# def make_float(s):
#     try:
#         return float(int(s))
#     except ValueError:
#         return float(s)

# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('results.html', name=name)


@app.route("/")
# def my_form():
#     return render_template("test.html")

def index():

    randomNumber = lambda: randint(0,len(data)-1)
    c = [data[randomNumber()] for i in range(0, 9)]
    # c = data[0]
    # for c in cs:
    #     if len(c['dimensions'])>0:
    #
    #         r = randint(0,len(c['dimensions'])-1)

    return render_template(
        'index.html',**locals())

@app.route('/', methods=['POST'])
def my_form_post():
    # l = make_float(request.form['length'])
    # w = make_float(request.form['width'])
    # h = make_float(request.form['height'])


    l = request.form['length']
    w = request.form['width']
    h = request.form['height']

    try:
        values=[float(l),float(w),float(h)]
        pf = my_c.the_perfect_fit_values(values,3.0)
        possibles = pf[0][3]
        possibles_text = 'There are '+str(len(possibles))+ ' containers that are within '+ str(pf[1])+ '\" of your space: '+ str(values[0])+'" x '+ str(values[1])+'" x '+ str(values[2])+'"'
        text = 'Containers closest to ' + str(values[0])+'" x '+ str(values[1])+'" x '+ str(values[2])+'"'
        # dimensions_text = str(Fraction(p[0]['new dimensions'][p[1]][0])) + 'x'
        p = possibles[0]
        p_0to9 = possibles[:21]
        return render_template('results.html',**locals())
    except:
        return render_template('index.html',**locals())
    # return render_template('results.html', name=possibles_text)

    # return possibles_text

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    # app.run(host='0.0.0.0', port=80)
    app.debug = False
    app.run()
