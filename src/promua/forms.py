from wtforms import Form, StringField, PasswordField, validators, TextField
from promua import models


class UserForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=20)])
    password = PasswordField("Password")
    email = StringField("E-Mail", [validators.Length(min=5)])

    def validate(self):
        #if not Form.validate(self):
        #    return False
        user = models.Users.query.filter_by(username=self.username.data).first()
        if user or len(unicode(self.password.data)) < 6:
            self.username.errors = 'This user already exists'
            self.password.errors = 'Password must contain more then 6 simb.'
            return False
        return True





