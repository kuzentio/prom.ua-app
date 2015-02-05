import hashlib

from flask import request, redirect, render_template, make_response, jsonify
from flask.ext.login import login_user, current_user, logout_user, login_required

from promua import models, utils
from promua.app import app, login_manager
from promua.forms import AuthorizationForm, RegistrationForm
from promua.models import db


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
    if request.method == 'POST':
        if not current_user.is_authenticated():
            raise Exception('Forbidden')
        import ipdb; ipdb.set_trace()
        answer = models.Answers(who_response_id=current_user.id, question_id=question_id, text_answer=request.form['answer'])
        db.session.add(answer)
        db.session.commit()
        return redirect('/question/%s/' % question_id)

    question = models.Questions.query.get(question_id)

    answers = db.session.query(
        models.Answers,
        models.Users,
    ).filter_by(
        question_id=question_id
    ).join(
        models.Users,
    ).all()

    voted_answers = []

    if current_user.is_authenticated():
        query = db.session.query(
            models.Votes
        ).filter(
            models.Votes.answer_id.in_([a.Answers.id for a in answers]),
        ).filter_by(
            user_id=current_user.id,
        )
        voted_answers = [a[0] for a in query.values('answer_id')]

    return render_template(
        "question.html",
        user=current_user,
        question=question,
        answers=answers,
        voted_answers=voted_answers,
    )


@app.route('/answers/<int:answer_id>/vote/', methods=['POST'])
@login_required
def question_vote(answer_id):
    answer = models.Answers.query.get(answer_id)
    if models.Votes.query.filter_by(user_id=current_user.id, answer_id=answer.id).count():
        return jsonify({"success": False})
    answer.votes += 1
    vote = models.Votes(user_id=current_user.id, answer_id=answer.id)
    db.session.add(answer)
    db.session.add(vote)
    db.session.commit()
    return jsonify({"success": True})


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)
    errors = {}
    if request.method == 'POST':
        if not form.validate():
            return render_template("registration.html", form=form, errors=form.errors)
        salt = utils.random_string(5)
        password = hashlib.sha224(form.password.data + salt).hexdigest()
        user = models.Users(username=form.username.data, password=password, salt=salt, email=form.email.data)
        db.session.add(user)
        db.session.commit()
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
