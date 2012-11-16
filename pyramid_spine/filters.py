from pyramid.threadlocal import get_current_request

from pyramid_spine.utils import utc
def route_path_filter(route_name, *elements, **kw):
    request = get_current_request()
    return request.route_path(route_name, *elements, **kw)

def static_path_filter(path, **kw):
    request = get_current_request()
    return request.static_path(path, **kw)

def localtime(dt):
    if dt is None:
        return dt
    request = get_current_request()
    tz = request.timezone
    if not dt.tzinfo:
        #assuming it's in UTC (THIS IS SO WRONG)
        return dt
    dt = dt.astimezone(tz)
    if hasattr(tz, 'normalize'):
        # available for pytz time zones
        dt = tz.normalize(dt)
    return dt

def strftime(dt, fmt):
    return dt.strftime(fmt)

