from flask import Module
from flask import redirect,request,session
from flask import render_template

from LanguageExplorer.model import User

login = Module(__name__)

# TODO(a33kuo): Ask user to set default material language.
@login.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None:
            error = 'This email is already registered.'
            return render_template('register.html', error=error)
        else:
            user = User(email, password, role)
            user.add()
            session['user_name'] = request.form['email'].split('@')[0]
            session['user_id'] = user.id
            session['user_language'] = request.form['lang']
            session['user_role'] = user.role
            return redirect('/')
    else:
        return render_template('register.html')

# TODO(a33kuo): Send out confirmation email after registration.
@login.route("/login", methods=['GET', 'POST'])
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
            session['user_name'] = request.form['email'].split('@')[0]
            session['user_id'] = user.id
            session['user_language'] = request.form['lang']
            session['user_role'] = user.role
            return redirect('/')
    else:
        return render_template('login.html')

@login.route("/logout")
def logout():
    if session.get('user_name'):
        del session['user_name']
    if session.get('user_id'):
        del session['user_id']
    if session.get('user_language'):
        del session['user_language']
    if session.get('user_role'):
        del session['user_role']
    session.modified = True
    return redirect('/')
