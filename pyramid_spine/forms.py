from pyramid.threadlocal import get_current_registry
from wtforms import Form, TextField, PasswordField, validators
from pyramid_mailer import get_mailer
from pyramid.renderers import render
from pyramid_spine.utils import int_to_base62
from pyramid_spine.tokens import token_generator

from pyramid_spine.models import user_factory
class SignupForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=256), validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    email = TextField('Email', [validators.Required(), validators.Email()])
    password = PasswordField('Password', [validators.Required()])

    def validate(self):
        print 'validating'
        registry = get_current_registry()
        User = user_factory(registry)
        rv = Form.validate(self)
        print self.errors
        if not rv:
            print 'returing false'
            return False

        user = User.query.filter_by(
            email=self.email.data).first()
        print user
        if user is None:
            print 'unknown email'
            self.email.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            print 'invalid password'
            self.password.errors.append('Invalid password')
            return False
        print 'what'
        self.user = user
        return True

class PasswordResetForm(Form):
    email = TextField('Email', [validators.Required(), validators.Email()])

    def save(self, request):
        mailer = get_mailer(request)
        settings = request.registry.settings

        subject = 'Password reset for buckit.io'
        base_id = int_to_base62(self.user.id)
        token = token_generator.create_token(self.user)
        context = {
            'domain': 'buckit.io',
            'protocol': 'https',
            'base_id': base_id,
            'token': token
        }
        body = render('spine/password_reset_email.html', context, request=request)
        message = Message(
            subject=subject,
            sender=settings.get('mail_sender'),
            recipients=[self.email.data],
            body=body)
        mailer.send(message)


class PasswordSetForm(Form):
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

    def save(self, user):
        user.set_password(self.password.data)
        return user
