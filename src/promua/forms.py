from wtforms import Form, StringField


class UserForm(Form):
    username = StringField("Username")
    password = StringField("Password")
    email = StringField("E-Mail")

