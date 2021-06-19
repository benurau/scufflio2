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

@app.route('/gues_coords', methods = ['POST', 'GET'])
def diez():
    request.method = 'GET'
    #request_data = request.json
    d = {"currX": coordsx}
    return jsonify(d)


@app.route('/scrib',methods = ['POST', 'GET'])
def login():
    global coordsx
    global coordsy

    if request.method == "POST":
      request_data = request.json

      coordsx.append(request_data["currX"])
      print(request.data)
      coordsy.append(request_data["currY"])

      if len(coordsx) > 1000:
        print(coordsx)
        plt.scatter(x=coordsx, y=coordsy)
        plt.show()

    elif request.method == "GET":
      d = {"currX": coordsx}
      print(coordsx)
      return jsonify(d)



if __name__ == "__main__":
  app.run()