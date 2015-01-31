from flask import Flask
from promua.forms import UserForm

from flask import request, redirect, render_template, make_response

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../app.db'
app.debug = True

@app.route('/', methods=['GET'])
def main():
    assert False, 123

@app.route('/registration/', methods=['GET'])
def registration():
    form = UserForm()

    return render_template("registration.html", form=form, errors='Might be errors')
