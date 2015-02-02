from flask import request, redirect, render_template, make_response
import hashlib
from flask.ext.login import login_user, current_user, logout_user
from promua.app import app, login_manager
from promua.forms import AuthorizationForm, RegistrationForm
from promua import models
from promua.models import db
from utils import utils


@login_manager.user_loader
def load_user(user_id):
    return models.Users.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def main():
    questions = db.session.query(models.Questions, models.Users).join(models.Users, models.Questions.who_ask_id == models.Users.id).all()
    if current_user.is_authenticated():
        if request.method == 'POST':
            question = models.Questions(who_ask_id=current_user.id, text_question=request.form['question'])
            db.session.add(question)
            db.session.commit()
            return redirect('/')
        return render_template("main.html", questions=questions, user_active=True)
    return render_template("main.html", questions=questions, user_active=False)


@app.route('/question/<int:question_id>/', methods=['GET', 'POST'])
def questions(question_id):
    question = models.Questions.query.get(question_id)
    answers = db.session.query(models.Answers, models.Users).\
        filter_by(question_id=question_id).\
        join(models.Users, models.Answers.who_response_id == models.Users.id).all()
    if current_user.is_authenticated():
        if request.method == 'POST':
            answer = models.Answers(who_response_id=current_user.id, question_id=question_id, text_answer=request.form['answer'])
            db.session.add(answer)
            db.session.commit()
            return redirect('/question/%s/' % question_id)
        return render_template("question.html", question=question, answers=answers, user_active=True)
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
        login_user(user)

        return redirect('/')

    return render_template("registration.html", form=form, errors=errors)


@app.route('/auth/', methods=['GET', 'POST'])
def authorization():
    errors = {}
    form = AuthorizationForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template("auth.html", form=form, errors=form.errors)
        user = models.Users.query.filter_by(username=form.username.data).first()
        login_user(user)

        return redirect('/')

    return render_template("auth.html", form=form, errors=errors)


@app.route('/exit/', methods=['GET', 'POST'])
def exit():
    logout_user()
    return redirect('/')

