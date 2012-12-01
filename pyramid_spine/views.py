from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPForbidden, HTTPFound, HTTPUnauthorized
from pyramid.security import unauthenticated_userid
from pyramid.security import forget, remember

from pyramid_spine.forms import SignupForm, LoginForm
"""
@view_defaults(renderer='login.mak')
class LoginView(object):
    def __init__(self, request):
        self.request = request
 
    def get_login_url(self):
        login_url = self.request.route_url('login')
        return login_url
 
    @view_config(context=HTTPForbidden)
    @view_config(route_name='login')
    def login(self):
        login_url = self.get_login_url()
        # more code goes here
        return dict(url=login_url)
"""

class AuthHandler(object):
    def __init__(self, request):
        self.request = request
        self.User = request.registry.spine_auth_class

@view_defaults(renderer='signup.html')
class SignupView(AuthHandler):

    @view_config(route_name='spine.signup', request_method='GET')
    def get(self):
        return {}

    @view_config(route_name='spine.signup', request_method='POST')
    def post(self):
        return {}

@view_defaults(renderer='login.html')
class LoginView(AuthHandler):
    @view_config(context=HTTPForbidden)
    @view_config(route_name='spine.login', request_method='GET')
    def get(self):
        form = LoginForm()
        return {'form': form}

    @view_config(route_name='spine.login', request_method='POST')
    def post(self):
        form = LoginForm(self.request.POST)
        if form.validate():
            #login and redirect
            pass
        return {'form': form}

def logout(request):
    headers = forget(request)
    # Redirect.
    location = request.route_path('spine.login')
    return HTTPFound(location=location, headers=headers)


