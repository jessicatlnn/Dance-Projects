from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Here will appear the dance project application"