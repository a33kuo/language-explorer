from flask import Flask
from flask import render_template

from LanguageExplorer.model import User

app = Flask(__name__)

@app.route("/")
def main():
    # TODO: Add new concepts and assertions.
    return render_template('index.html')
