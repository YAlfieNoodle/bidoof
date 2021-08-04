from flask import Flask, render_template
from threading import Thread
from oauth import Oauth

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html",discord_url=Oauth.discord_login_url)

@app.route("/login")
def login():
	return "yes"

def run():
  app.run(host='0.0.0.0',port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()