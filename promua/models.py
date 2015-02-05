from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from promua.app import app

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(80))
    salt = db.Column(db.String(10))
    email = db.Column(db.String(20), unique=True)
    Questions = db.relationship('Questions', backref='users')
    Answers = db.relationship('Answers', backref='users')

    def get_id(self):
        return unicode(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    session_id = db.Column(db.String(20), nullable=False, unique=True)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    who_ask_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    text_question = db.Column(db.String(100))
    answer = db.relationship("Answers")


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    who_response_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    text_answer = db.Column(db.String(200))
    votes = db.Column(db.Integer, default=0)


class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey("answers.id"), nullable=False)
