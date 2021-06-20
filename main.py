#Import necessary libraries
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response,jsonify,request
from flask import g

app = Flask(__name__)

coordsx = []
coordsy = []


@app.route('/')
def index():
    return render_template("scib.html")

@app.route('/gues')
def gues():
    return render_template("quesser.html")

@app.route('/get_words')
def benu():
    words = ["benu","pp","dummy","small"]
    return jsonify(words)




@app.route('/scrib',methods = ['POST', 'GET'])
def login():
    global coordsx
    global coordsy

    if request.method == "POST":
      request_data = request.json

      coordsx.append(request_data["currX"])
      coordsy.append(request_data["currY"])
      print(request_data)
    elif request.method == "GET":
      d = {"currX": coordsx,
           "currY": coordsy
           }
      return jsonify(d)



if __name__ == "__main__":
  app.run()