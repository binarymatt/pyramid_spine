from pytz import timezone

from pyramid.settings import asbool
def csrf_tween_factory(handler, registry):
    pass

def timezone_tween_factory(handler, registry):
    if asbool(registry.settings.get('use_tz')):
        def timezone_tween(request):
            request.timezone = timezone(registry.settings.get('timezone'))
            return handler(request)
        return timezone_tween
    return handler
