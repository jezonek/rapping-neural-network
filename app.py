from flask import Flask

from serve_done_text import serve_done_text as done_text

app = Flask(__name__)


@app.route("/")
def serve_done_text():
    text = done_text()
    if text:
        return '<html><body>{}</body></html>'.format("<br>".join(text))
    else:
        return '<html><body>Generating text... Refresh after some time</body></html>'
