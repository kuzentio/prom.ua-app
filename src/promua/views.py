from flask import request, redirect, render_template, make_response
import hashlib
from promua.app import app
from promua.forms import AuthorizationForm, RegistrationForm
from promua import models
from promua.models import db
from utils import utils


@app.route('/', methods=['GET', 'POST'])
def main():
    questions = db.session.query(models.Questions, models.Users).join(models.Users, models.Questions.who_ask_id == models.Users.id).all()
    if 'session_id' in request.cookies and request.cookies['session_id'] == models.Sessions.query.filter_by(session_id=request.cookies['session_id']).first().session_id:
        session = models.Sessions.query.filter_by(session_id=request.cookies['session_id'])
        if request.method == 'POST':
            question = models.Questions(who_ask_id=session[0].user_id, text_question=request.form['question'])
            db.session.add(question)
            db.session.commit()
            return redirect('/')

        return render_template("main.html", questions=questions, active=True)
    return render_template("main.html", questions=questions, active=False)


@app.route('/questions/<int:question_id>/', methods=['GET'])
def questions(question_id):
    question = models.Questions.query.get(question_id)
    answers = db.session.query(models.Answers, models.Users).\
        filter_by(question_id=question_id).\
        join(models.Users, models.Answers.who_response_id == models.Users.id).all()


    return render_template("question.html", question=question, answers=answers)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    errors = {}
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template("registration.html", form=form, errors=form.errors)
        salt = utils.random_string(5)
        password = hashlib.sha224(form.password.data + salt).hexdigest()
        user = models.Users(username=form.username.data, password=password, salt=salt, email=form.email.data)
        db.session.add(user)
        db.session.commit()

        user = models.Users.query.filter_by(username=form.username.data).first()
        user_session = models.Sessions(session_id=utils.random_string(20), user_id=user.id)
        response = make_response(redirect('/'))
        response.set_cookie('session_id', user_session.session_id)
        db.session.add(user_session)
        db.session.commit()

        return response

    return render_template("registration.html", form=form, errors=errors)


@app.route('/auth/', methods=['GET', 'POST'])
def authorization():
    errors = {}
    form = AuthorizationForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template("auth.html", form=form, errors=form.errors)
        user = models.Users.query.filter_by(username=form.username.data).first()
        user_session = models.Sessions(session_id=utils.random_string(20), user_id=user.id)
        response = make_response(redirect('/'))
        response.set_cookie('session_id', user_session.session_id)
        db.session.add(user_session)
        db.session.commit()

        return response

    return render_template("auth.html", form=form, errors=errors)






