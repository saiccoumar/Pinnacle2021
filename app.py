
from flask import Flask, session, render_template, Response, request, redirect
from datetime import timedelta
import sqlite3
import utils
import numpy
import itertools
import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn import preprocessing
import svd4

statDir = './static/'
templateDir = './templates/'
# initialize a flask object
app = Flask(__name__,static_folder=statDir,
            template_folder=templateDir)

dbFile = 'movies3.db'
cached_results = None
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

@app.route("/autocompleteLIM/<term>")
def autocompleteLIM(term):
    con = sqlite3.connect(dbFile)
    cur = con.cursor()
    return utils.autocompleteLIM(con,term)

@app.route("/queryPearson/<search>", methods=["GET"])
def start(search):
    con = connect()
    cur = con.cursor()
    #returns recomendations in JSON form
    recs = utils.formatCorrelations(utils.calcCorrelations(cur,search,15000))
    return recs

@app.route("/querySVD/<search>", methods=["GET"])
def svdStart(search):
    con = connect()
    item = con.execute(f"select itemID from itemInfo where name='{search}'").fetchone()[0]
    global cached_results
    if cached_results:
        [p,q,data,dataDF] = cached_results
        prediction = svd4.predict_rating(p,q,1,item,dataDF) #TODO change 1 to random user
    # returns recomendations in JSON form
        return {"prediction":prediction}
    else:
        p,q,data,dataDF = svd4.SVD(1)
        p,q= svd4.SVDUpgrade(data, 1,p,q)
        cached_results= [p,q,data,dataDF]
        prediction = svd4.predict_rating(p,q,1,item,dataDF) #TODO change 1 to random user
    # returns recomendations in JSON form
        return {"prediction":prediction}
    
    
    # Temporary format of JSON
    # return {"items": [
    #     {
    #         "userID": 123,
    #         "affinity": 4.7
    #     },
    #     {
    #         "userID": 135,
    #         "affinity": 9.8
    #     }
    # ]}

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(debug=True)
