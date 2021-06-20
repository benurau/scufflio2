#Import necessary libraries
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response,jsonify,request
from flask import g

app = Flask(__name__)

coordsx = []
coordsy = []

class User:
    def __init__(self, ip):
        self.ip = ip
        self.points = 0
        self.n_painted = 0
        self.guessed_correct = False

    def add_points(self, points):
        self.points += points

    def add_painted(self):
        self.n_painted += 1

    def add_guessed_correct(self):
        self.guessed_correct = True



class Game():
    def __init__(self):
        self.round = 1
        self.players = []

    def add_player(self,user:User):
        self.players.append(user)

    def next_round(self):
        self.round += 1

    def get_current_round(self):
        return self.round

    def get_player_scores(self):
        players = [(x,x.points) for x in self.players]
        print(players)


@app.route('/')
def index():
    return render_template("scib.html")

@app.route('/gues')
def gues():
    return render_template("quesser.html")

@app.route('/get_words')
def benu():
    words = ["benu", "pp", "dummy", "small"]
    d = {"words": words}
    print(d)
    return jsonify(d)


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    print(request.remote_addr)
    #return jsonify({'ip': request.remote_addr}), 200


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