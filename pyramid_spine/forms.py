from pyramid.threadlocal import get_current_registry
from wtforms import Form, TextField, PasswordField, validators
from pyramid_mailer import get_mailer
from pyramid.renderers import render
from pyramid_spine.utils import int_to_base62
from pyramid_spine.tokens import token_generator


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
