import hashlib
from promua.app import app
from flask import request, redirect, render_template, make_response
from promua.forms import UserForm, AuthorizationForm
from promua import models
from promua.models import db
from promua import utils


@app.route('/', methods=['GET'])
def main():
    assert False, 123

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    errors = {}
    form = UserForm(request.form)
    if request.method == 'POST' and not form.validate():
        return render_template("registration.html", form=form, errors=form.errors)

    if request.method == 'POST' and form.validate():
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
    if request.method == 'POST' and not form.validate():
        return render_template("auth.html", form=form, errors=form.errors)

    if request.method == 'POST' and form.validate():
        user = models.Users.query.filter_by(username=form.username.data).first()
        user_session = models.Sessions(session_id=utils.random_string(20), user_id=user.id)
        response = make_response(redirect('/'))
        response.set_cookie('session_id', user_session.session_id)
        db.session.add(user_session)
        db.session.commit()

        return response

    return render_template("auth.html", form=form, errors=errors)






