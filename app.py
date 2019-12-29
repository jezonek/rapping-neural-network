from flask import Flask
from documented_model import main

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/train")
def train():
    main(4,True)
    return "<h1>Training started!</h1>"


if __name__== '__main__':
    app.run(threaded=True, port=5000)