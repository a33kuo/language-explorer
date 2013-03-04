from flask import Flask
from flask import session
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
    if session.get('user_name'):
        user = session['user_name']
    else:
        user = None
    return render_template('index.html', index_image=img_id, user_name=user)
