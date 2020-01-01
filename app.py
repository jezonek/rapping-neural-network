from flask import Flask

from documented_model import main

app = Flask(__name__)


@app.route("/")
def hello_world():
    rap="<br>".join(main(4,False))
    return "<html><body>{}</body></html>".format(rap)


if __name__ == '__main__':
    app.run(host="0.0.0.0",threaded=True, port=8000)
