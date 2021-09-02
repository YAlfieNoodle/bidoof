from flask import Flask, render_template,request, session,redirect
from threading import Thread
from oauth import Oauth
from routes.discord_oauth import DiscordOauth

app = Flask(__name__)
app.config["SECRET_KEY"] = "test123"

@app.route('/')
def home():
    return "Alive and well"



def run():
  app.run(host='0.0.0.0',port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()