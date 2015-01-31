import hashlib
from promua.app import app
from flask import request, redirect, render_template, make_response
from promua.forms import UserForm, AuthorizationForm
from promua import models
from promua.models import Users, db
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
        salt = utils.random_string(20)
        password = hashlib.sha224(form.password.data + salt).hexdigest()
        user = models.Users(username=form.username.data, password=password, salt=salt, email=form.email.data)
        db.session.add(user)
        db.session.commit()

        return redirect('/')

    return render_template("registration.html", form=form, errors=errors)


@app.route('/auth/', methods=['GET', 'POST'])
def authorization():
    errors = {}
    form = AuthorizationForm(request.form)
    if request.method == 'POST' and not form.validate():
        return render_template("auth.html", form=form, errors=form.errors)

    if request.method == 'POST' and form.validate():
        return redirect('/')

    return render_template("auth.html", form=form, errors=errors)






