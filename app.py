
from flask import Flask, session, render_template, Response, request, redirect
from datetime import timedelta
import sqlite3
import utils
import numpy
import itertools

statDir = './static/'
templateDir = './templates/'
# initialize a flask object
app = Flask(__name__,static_folder=statDir,
            template_folder=templateDir)

dbFile = 'movies.db'

def connect(db = dbFile):
    con = sqlite3.connect(dbFile)
    class myCorr:
        def __init__(self):
            self.count = 0
            self.list1 = []
            self.list2 = []
        def step(self, value1,value2):
            self.list1.append(value1)
            self.list2.append(value2)
        def finalize(self):
            #print(self.list1[:10])
            #print(self.list2[:10])
            if len(self.list1) and len(self.list2):
                self.correlation = numpy.corrcoef(self.list1,self.list2)[0][1]
            else:
                self.correlation = 0.0
            return self.correlation

    con.create_aggregate("corr", 2, myCorr)
    return con



@app.route('/')
def index():
    return render_template("index.html")

@app.route("/autocomplete/<term>")
def autocomplete(term):
    con = sqlite3.connect(dbFile)
    cur = con.cursor()
    return utils.autocomplete(con,term)

@app.route("/query/<search>", methods=["GET"])
def start(search):
    con = connect()
    cur = con.cursor()
    #returns recomendations in JSON form
    recs = utils.formatCorrelations(utils.calcCorrelations(cur,search,10))
    return recs

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(debug=True)
