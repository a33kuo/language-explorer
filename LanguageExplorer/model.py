from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from validate_email import validate_email

from LanguageExplorer.util import enum

db = SQLAlchemy()
AGE_GROUP = enum('kid', 'adult')

def connect_db(app):
    db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.Integer)
    ROLE = enum('admin', 'teacher', 'student')

    def __init__(self, email, password, role=ROLE.student):
        if not validate_email(email):
            raise ValueError('Email format is not valid.')
        if len(email) > 120:
            raise ValueError('Email length exceeds 120 characters.')
        if len(password) > 120:
            raise ValueError('Password length exceeds 120 characters.')
        self.email = email
        passwd_hash = pwd_context.encrypt(password, category='admin')
        self.password = passwd_hash
        self.role = role

    def __repr__(self):
        return '<User:%r %r>' % (self.id, self.username)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, password=None, role=None):
        if password != None:
            passwd_hash = pwd_context.encrypt(password, category='admin')
            self.password = passwd_hash
        elif role != None:
            self.role = role
        if password != None or role != None:
            db.session.commit()

    def get_role_name(self, role):
        if role < len(ROLE.reverse_mapping.keys()) and role >= 0:
            return ROLE.reverse_mapping[role]
        else:
            raise KeyError("No such role id.");

    def check_password(self, password):
        return pwd_context.verify(password, self.password)
