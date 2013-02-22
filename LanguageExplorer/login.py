from flask import Module
from flask import redirect,request,session
from flask import render_template

from LanguageExplorer.model import User

login = Module(__name__)

@login.route("/register/")
def register():
    pass

@login.route("/login/", methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
      user = User.query.filter_by(email=request.form['email']).first()
      if user is None:
        error = 'No such email.'
        return render_template('login.html', error=error)
      if not user.check_password(request.form['password']):
        error = 'Invalid password.'
        return render_template('login.html', error=error)
      else:
        session['user_email'] = request.form['email']
        flash('You have logged in.')
        return redirect('/')
    return render_template('login.html')

@login.route("/logout/")
def logout():
    if session.get('user_email'):
        del session['user_email']
    session.modified = True
    return redirect('/')
