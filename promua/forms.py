import hashlib

from wtforms import Form, StringField, PasswordField, validators, TextField
from promua import models, utils


class RegistrationForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=20)])
    password = PasswordField("Password")
    email = StringField("E-Mail", [validators.Length(min=5)])

    def validate(self):
        user = models.Users.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors = 'This user already exists'
            return False
        if len(unicode(self.password.data)) < 6:
            self.password.errors = 'Password must contain more then 6 simb.'
            return False
        return True


class AuthorizationForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")

    def validate(self):
        user = models.Users.query.filter_by(username=self.username.data).first()
        if not Form.validate(self):
            return False
        if not user:
            self.username.errors = "We don't know about %s, you can" %self.username.data
            return False
        elif user.password != hashlib.sha224(unicode(self.password.data) + user.salt).hexdigest():
            self.password.errors = "Enter correct username of password."
            return False
        return True
