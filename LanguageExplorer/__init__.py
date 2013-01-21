from flask import Flask

from LanguageExplorer.model import User

app = Flask(__name__)

@app.route("/")
def main():
    return 'Language Explorer is under construction!'
