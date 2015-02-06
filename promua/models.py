from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from promua.app import app

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(80))
    salt = db.Column(db.String(10))
    email = db.Column(db.String(20), unique=True)
    question = relationship('Questions', backref="user")
    answer = relationship('Answers', backref="user")

    def get_id(self):
        return unicode(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    who_ask_id = db.Column(db.Integer, ForeignKey("users.id"))
    text_question = db.Column(db.String(100))
    answer = relationship("Answers", backref="questions")


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    who_response_id = db.Column(db.Integer, ForeignKey("users.id"))
    question_id = db.Column(db.Integer, ForeignKey("questions.id"))
    text_answer = db.Column(db.String(200))
    votes = db.Column(db.Integer, default=0)


class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    answer_id = db.Column(db.Integer, ForeignKey("answers.id"))
