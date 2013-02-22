from flask import Flask
from flask import render_template

from LanguageExplorer.model import User

import random

app = Flask(__name__)

from login import login
app.register_module(login)

@app.route("/")
def main():
    # TODO: Add new concepts and assertions.
    img_id = random.randint(1, 7)
    return render_template('index.html', index_image=img_id)
