
from flask import Flask, session, render_template, Response, request, redirect
from datetime import timedelta
import sqlite3
import utils
import numpy

statDir = './static/'
templateDir = './templates/'
# initialize a flask object
app = Flask(__name__,static_folder=statDir,
            template_folder=templateDir)

def connect(db = 'amazon.db'):
    con = sqlite3.connect('amazon.db')
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
    return render_template("home.html")

@app.route("/query",methods =['POST','GET'])
def start():
    if request.method == 'POST':
        product = request.form["product"]
        con = connect()
        cur = con.cursor()
        #returns recomendations in JSON form
        recs = utils.formatCorrelations(utils.calcCorrelations(cur,product,10))
        return recs
    else:
        return "do not use get"

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(debug=True)
