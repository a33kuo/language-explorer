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
    password = db.Column(db.String(512))
    role = db.Column(db.Integer)
    ROLE = enum('admin', 'teacher', 'student')

    def __init__(self, email, password, role=ROLE.student):
        if not validate_email(email):
            raise ValueError('Email format is not valid.')
        if len(email) > 120:
            raise ValueError('Email length exceeds 120 characters.')
        passwd_hash = pwd_context.encrypt(password, category='admin')
        if len(passwd_hash) > 512:
            raise ValueError('Password length exceeds limit.')
        self.email = email
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


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    description = db.Column(db.String(512))
    contexts = db.relationship('Context', backref='language', lazy='dynamic')
    concepts = db.relationship('Context', backref='language', lazy='dynamic')

    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __repr__(self):
        return '<Language:%r>' % (self.code)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, code=None, description=None):
        if code != None:
            self.code = code
        elif description != None:
            self.description = description
        if code != None or description != None:
            db.session.commit()


concept_context = db.Table('concept_context',
    db.Column('concept_id', db.Integer, db.ForeignKey('context.id')),
    db.Column('context_id', db.Integer, db.ForeignKey('concept.id'))
)

class Context(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256), unique=True)
    ctype = db.Column(db.Integer)
    CONTEXT_TYPE = enum('location', 'event')
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))

    def __init__(self, text, lang_id, ctype=CONTEXT_TYPE.location):
        self.text = text
        self.ctype = ctype
        self.language_id = lang_id

    def __repr__(self):
        return '<Context:%r %r>' % (self.ctype, self.text)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, text=None, ctype=None, lang=None):
        if text != None:
            self.text = text
        elif ctype != None:
            self.ctype = ctype
        elif lang != None:
            self.language_id = lang
        if text != None or ctype != None or lang != None:
            db.session.commit()

    @staticmethod
    def get_context(text, lang):
        return db.session.query(Context).filter_by(text=text)\
                                        .filter_by(language_id=lang).one()


class Concept(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256), unique=True)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    concept_context = db.relationship('Context', secondary=concept_context, \
                                      backref=db.backref('concepts', \
                                                         lazy='dynamic'))

    def __init__(self, text, lang):
        self.text = text
        self.language_id = lang

    def __repr__(self):
        lang = Language.query.get(language_id)
        return '<Concept:%r/%r>' % (self.text, lang.code)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, text=None, lang=None):
        if text != None:
            self.text = text
        elif lang != None:
            self.language_id = lang
        if text != None or lang != None:
            db.session.commit()

    @staticmethod
    def get_context(text, lang):
        return db.session.query(Concept).filter_by(text=text)\
                                        .filter_by(language_id=lang).one()
