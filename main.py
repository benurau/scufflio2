#Import necessary libraries
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response,jsonify,request,redirect
from flask import g
import pandas as pd
import time
import random
import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.disabled = True

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
        self.round_time_left = 10
        self.current_painter = ""
        self.word_chosen = ""
        self.round_length = 7
        self.game_started = 0

    def add_player(self, user: User):
        self.players.append(user)

    def next_small_round(self):
        if len(self.order_list)>0:
            self.small_round += 1
            # Get last player of list
            self.current_painter = self.order_list[0]
            # Remove him from the list
            self.order_list.pop(0)
            print("Painter chosen:",self.current_painter.ip)
        else:
            print("Small rounds ended, next big round start")
            game1.update_order_list()
            self.current_painter = self.order_list[0]
            # Remove him from the list
            self.order_list.pop(0)
            print("Painter chosen:", self.current_painter.ip)




    def next_round(self):
        self.round += 1

    def get_current_round(self):
        return self.round

    def get_players(self):
        return self.players

    def get_player_scores(self):
        players = sorted([(x.ip, x.points) for x in self.players], key=lambda i: i[1], reverse=True)
        return players

    def player_guessed_correctly(self,ip):
        user = [x for x in self.players if x.ip == str(ip)][0]
        user.add_guessed_correct()
        print(user,"guessed correctly")


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

    def restart_timer(self):
        self.round_time_left = 10
        self.game_started = time.time()

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


game1 = Game()
w1 = Words("words.csv")

@app.route('/benupp')
def index():
    global game1
    print("User:",request.remote_addr,"connected")
    user1 = User(request.remote_addr)
    game1.add_player(user1)
    return render_template("scib.html")


@app.route('/gues')
def gues():
    return render_template("quesser.html")

@app.route('/')
def home():
    return render_template("home.html")    


@app.route('/get_words', methods = ['GET'])
def benu():
    global w1
    words = w1.get_n_words(10)
    d = {"words": words}
    return jsonify(d)


@app.route('/start_game', methods = ['POST'])
def start_game():
    global game1
    print(request.remote_addr)
    request_data = request.json
    print(request_data)
    player_name = request_data["word"]
    user1 = User(player_name)
    game1.add_player(user1)
    print("players this round",game1.get_players())
    # Set order of players
    game1.next_small_round()
    print(game1.round_time_left)
    game1.game_started = time.time()
    print(game1.game_started)
    """
    while game1.round_time_left > 0:
        game1.tick()
        time.sleep(1)
        print(game1.round_time_left)"""



@app.route('/benupp',methods = ['POST',"GET"])
def start_gameaaa():
    return render_template("scib.html")


@app.route("/user_chose_word", methods=["POST"])
def chosen_word():
    global game1
    print(request)
    if request.method == "POST":
        request_data = request.json
        print(request_data["chose_word"],"chosen")
        game1.chose_word(request_data["chose_word"])


@app.route("/chat_gues", methods=["POST","GET"])
def chat_gues():
    global game1
    print(game1)
    #game1.chose_word('penis')
    request_data = request.json
    print(request_data)
    guesser_ip = request.remote_addr
    print(guesser_ip)
    if request_data["word"] == game1.word_chosen:
       game1.player_guessed_correctly(guesser_ip)
       print('CORRECT')
       print(game1.has_guessed_correctly())
       d = {"Correct": game1.word_chosen}
       return jsonify(d)
    else:
        print("Not match:",request_data["word"], "!=", game1.word_chosen)


@app.route('/scrib',methods = ['POST', 'GET'])
def login():
    global coordsx
    global coordsy
    global color
    global game1
    if request.method == "POST":
      request_data = request.json

      coordsx.append(request_data["currX"])
      coordsy.append(request_data["currY"])
      color = request_data["color"]
      print(round((game1.game_started + 10) - time.time(),2))
      if round((game1.game_started + 10) - time.time(),2)<0:
          print("made it")
          #return redirect("http://127.0.0.1:5000/",code=307)
          return jsonify({"gameend": True, "time": round((game1.game_started + 10) - time.time(), 2)})
      else:
          return jsonify({"gameend":False,"time":round((game1.game_started + 10) - time.time(),2)})

    elif request.method == "GET":
      #print(time.time(), "-", game1.game_started + 10)
      time_left = round((game1.game_started + 10) - time.time(),5)
      if time_left<0:
          game1.next_small_round()
          game1.restart_timer()
          print("BEFORE RED")
          if request.remote_addr == game1.current_painter:
            return redirect("http://127.0.0.1:5000/")

      d = {"currX": coordsx,
           "currY": coordsy,
           "color": color,
           "time_left": time_left
           }
      return jsonify(d)


if __name__ == "__main__":
  app.run(host="0.0.0.0")