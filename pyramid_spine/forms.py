from wtforms import Form, TextField, PasswordField, validators
class SignupForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=256), validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    email = TextField('Email Address', [validators.Length(max=256), validators.Email(), validators.Required()])
    password = PasswordField('Password', [validators.Required()])
