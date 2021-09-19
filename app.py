
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

def predict_rating(user_mat, movie_mat, user_id, movie_id,data):
    
    # Use the training data to create a series of users and movies that matches the ordering in training data
    user_ids_series = np.array(data.index)
    movie_ids_series = np.array(data.columns)
    
    # User row and Movie Column
    user_row = np.where(user_ids_series == user_id)[0][0]
    movie_col = np.where(movie_ids_series == movie_id)[0][0]
    
    # Take dot product of that row and column in U and V to make prediction
    pred = np.dot(user_mat[user_row, :], movie_mat[:, movie_col])
    
    return pred

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/autocomplete/<term>")
def autocomplete(term):
    con = sqlite3.connect(dbFile)
    cur = con.cursor()
    return utils.autocomplete(con,term)

@app.route("/queryPearson/<search>", methods=["GET"])
def start(search):
    con = connect()
    cur = con.cursor()
    #returns recomendations in JSON form
    recs = utils.formatCorrelations(utils.calcCorrelations(cur,search,10))
    return recs

@app.route("/querySVD/<search>", methods=["GET"])
def start(search):
    con = connect()
    p,q,data,dataDF=svd4.SVD(4,con)
    p,q= svd4.SVDUpgrade(data, 3,p,q)
    prediction = predict_rating(p,q,1,3448,dataDF) #TODO change 1 to random user
    #returns recomendations in JSON form
    return {"prediction":prediction}

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(debug=True)
