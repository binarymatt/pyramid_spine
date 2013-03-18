from pyramid.security import NO_PERMISSION_REQUIRED as PUBLIC
from sqlalchemy import engine_from_config

from .models import (
    initialize_sql,
    get_user
)
from .views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
)
def register_user_class(config, klass):
    def register():
        registry = config.registry
        if hasattr(registry, 'spine_auth_class'):
            return
        registry.spine_auth_class = klass
    config.action(('spine-auth-classs', klass), register)

def add_password_reset_view(config, route_base="/password_reset"):
    config.add_route('spine.password_reset', route_base)
    config.add_route('spine.password_reset_done', '%s/done/' % route_base)
    config.add_route('spine.password_reset_confirm', '%s/confirm/' % route_base)
    config.add_route('spine.password_reset_complete', '%s/complete/' % route_base)

    config.add_view(password_reset, route_name='spine.password_reset', renderer='spine/password_reset.html', permission=PUBLIC)
    config.add_view(password_reset_done, route_name='spine.password_reset_done', renderer='spine/password_reset_done.html', permission=PUBLIC)
    config.add_view(password_reset_confirm, route_name='spine.password_reset_confirm', renderer='spine/password_reset_confirm.html', permission=PUBLIC)
    config.add_view(password_reset_complete, route_name='spine.password_reset_complete', renderer='spine/password_reset_complete.html', permission=PUBLIC)
def includeme(config):
    settings = config.registry.settings
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config.add_directive('add_spine_user_class', register_user_class)
    config.add_directive('add_password_reset_view', add_password_reset_view)
    config.set_request_property(get_user, 'user', reify=True)

    config.include('pyramid_jinja2')
    config.add_renderer('.html', factory='pyramid_jinja2.renderer_factory')
    config.add_jinja2_search_path("pyramid_spine:templates")

    config.include('pyramid_mailer')
    config.scan()

