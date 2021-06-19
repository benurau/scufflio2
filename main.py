#Import necessary libraries
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response,jsonify,request


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
  print(coordsx)
  return jsonify(d)



@app.route('/scrib',methods = ['POST', 'GET'])
def login():


  #request.method = 'POST'
  request_data = request.json

  if request.method == "POST":
    coordsx.append(request_data["currX"])
    print(request.data)
    coordsy.append(request_data["currY"])

    if len(coordsx) > 1000:
      print(coordsx)
      plt.scatter(x=coordsx, y=coordsy)
      plt.show()

  if request.method == "GET":
    request.method = 'GET'
    d = {"currX": coordsx}
    print(coordsx)
    return jsonify(d)




if __name__ == "__main__":
  app.run()