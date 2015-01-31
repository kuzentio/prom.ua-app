from promua.app import app
from flask import request, redirect, render_template, make_response
from promua.forms import UserForm
from promua import models
from promua.models import Users, db


@app.route('/', methods=['GET'])
def main():
    assert False, 123

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = UserForm(request.form)
    if request.method == 'POST' and not form.validate():
        return render_template("registration.html", form=form, errors=form.errors)

    if request.method == 'POST' and form.validate():
        user = models.Users(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/')


    return render_template("registration.html", form=form)


