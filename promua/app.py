from flask import Flask
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../app.db'
app.debug = True
app.secret_key = 'qwerty'

login_manager = LoginManager()
login_manager.init_app(app)
