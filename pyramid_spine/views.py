from pyramid.view import view_config, view_defaults
from pyramid.security import NO_PERMISSION_REQUIRED as PUBLIC
from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget, remember

from pyramid_spine.forms import (
    LoginForm,
    PasswordResetForm,
    PasswordSetForm
)
from pyramid_spine.events import LoginEvent
from pyramid_spine.utils import base62_to_int
from pyramid_spine.tokens import token_generator
from pyramid_spine.models import user_factory, DBSession

class AuthHandler(object):
    def __init__(self, request):
        self.request = request
        self.User = request.registry.spine_auth_class

@view_defaults(renderer='spine/login.html')
class LoginView(AuthHandler):
    @view_config(route_name='spine.login', request_method='GET', permission=PUBLIC)
    def get(self):
        form = LoginForm()
        return {'form': form}

    @view_config(route_name='spine.login', request_method='POST', permission=PUBLIC)
    def post(self):
        form = LoginForm(self.request.POST)
        print 'test'
        if form.validate():
            print 'test'
            #login and redirect
            user = form.user
            headers = remember(self.request, user.id)
            self.request.registry.notify(LoginEvent(self.request))
            location = self.request.route_path('search')
            return HTTPFound(location=location, headers=headers)
        return {'form': form}

@view_config(route_name='spine.logout')
def logout(request):
    headers = forget(request)
    location = request.route_path('account.login')
    return HTTPFound(location=location, headers=headers)

#@view_config(route_name='spine.password_reset', renderer='spine/password_reset.html', permission=PUBLIC)
def password_reset(request):
    form = PasswordResetForm(request.POST)
    if request.method == "POST" and form.validate():
        form.save(request)
        return HTTPFound(location=request.route_path('account.password_reset_done'))
    return {'form': form}

# - password_reset_done shows a success message for the above
#@view_config(route_name='account.password_reset_done', renderer='account/password_reset_done.html', permission=PUBLIC)
def password_reset_done(request):
    return {}

# - password_reset_confirm checks the link the user clicked and
#   prompts for a new password
#@view_config(route_name='account.password_reset_confirm', renderer='account/password_reset_confirm.html', permission=PUBLIC)
def password_reset_confirm(request):
    User = user_factory(request.registry)
    base_id = request.matchdict['base_id']
    id = base62_to_int(base_id)
    token = request.matchdict['token']
    user = User.query.filter_by(id=id).first()
    #check token
    if user is not None and token_generator.check_token(user, token):
        form = PasswordSetForm(request.POST)
        if request.method == "POST" and form.validate():
            user = form.save(user)
            session = DBSession()
            #session.add(user)
            session.flush()
            return HTTPFound(location=request.route_path('account.password_reset_complete'))
    else:
        form = None
    return {'form': form, 'base_id': base_id, 'token': token}
# - password_reset_complete shows a success message for the above
#@view_config(route_name='account.password_reset_complete', renderer='account/password_reset_complete.html', permission=PUBLIC)
def password_reset_complete(request):
    return {}


