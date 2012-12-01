from sqlalchemy import engine_from_config

from .models import (
    initialize_sql
)
def register_user_class(config, klass):
    def register():
        registry = config.registry
        if hasattr(registry, 'spine_auth_class'):
            return
        registry.spine_auth_class = klass
    config.action(('spine-auth-classs', klass), register)

def includeme(config):
    settings = config.registry.settings
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config.add_directive('add_spine_user_class', register_user_class)

