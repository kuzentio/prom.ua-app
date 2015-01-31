from flask.ext.sqlalchemy import SQLAlchemy

from promua.app import app

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(20))
    salt = db.Column(db.String(10))
    email = db.Column(db.String(120), unique=True)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    who_ask_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    text_question = db.Column(db.String(100))


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id", ondelete='CASCADE'), nullable=False)
    text_answer = db.Column(db.String(200))


    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
