#Import necessary libraries
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response,jsonify,request
from flask import g
import pandas as pd
import time
import random


app = Flask(__name__)

coordsx = []
coordsy = []
color = "black"


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


class Game:

    def __init__(self):
        self.round = 1
        self.small_round = 1
        self.players = []
        self.order_list = []
        self.round_time_left = 0
        self.current_painter = ""
        self.word_chosen = ""
        self.round_length = 7

    def add_player(self, user: User):
        self.players.append(user)

    def next_small_round(self):
        self.small_round += 1
        # Get last player of list
        self.current_painter = self.order_list[0]
        # Remove him from the list
        self.order_list.pop(0)
        print("Painter chosen:",self.current_painter.ip)

    def next_round(self):
        self.round += 1

    def get_current_round(self):
        return self.round

    def get_players(self):
        return self.players

    def get_player_scores(self):
        players = sorted([(x.ip, x.points) for x in self.players], key=lambda i: i[1], reverse=True)
        return players

    def start_small_round(self):
        self.round_time_left = self.round_length
        print("Round started")

    def tick(self):
        self.round_time_left -= 1
        print(self.round_time_left)
        if self.round_time_left == 0:
            return True

    def update_order_list(self):
        self.order_list = [x for x in self.players]
        return self.order_list

    def has_guessed_correctly(self):
        return [(x.ip,x.guessed_correct) for x in self.players]

    def guess(self, User, guess):
        if guess == self.word_chosen:
            User.add_guessed_correct()

    def chose_word(self,word):
        self.word_chosen = word


class Words:
    def __init__(self,file):
        df = pd.read_csv(file)
        self.words = []
        for x in df["word"]:
            self.words.append(x)
        self.word_count = len(self.words)
        print(self.word_count)

    def get_n_words(self,n):
        out_list = []
        for x in range(n):
            rng = random.randint(0,self.word_count)
            out_list.append(self.words[rng])
            self.words.pop(rng)
        return out_list




@app.route('/')
def index():
    return render_template("scib.html")

@app.route('/gues')
def gues():
    return render_template("quesser.html")

@app.route('/home')
def home():
    return render_template("home.html")    


@app.route('/get_words', methods = ['GET'])
def benu():
    words = ["benu", "pp", "dummy", "small"]
    d = {"words": words}
    return jsonify(d)


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    print(request.remote_addr)
    #return jsonify({'ip': request.remote_addr}), 200


@app.route('/scrib',methods = ['POST', 'GET'])
def login():
    global coordsx
    global coordsy
    global color

    if request.method == "POST":
      request_data = request.json

      coordsx.append(request_data["currX"])
      coordsy.append(request_data["currY"])
      color = request_data["color"]
      print(request_data)

    elif request.method == "GET":
      d = {"currX": coordsx,
           "currY": coordsy,
           "color": color
           }
      return jsonify(d)


if __name__ == "__main__":
  app.run()