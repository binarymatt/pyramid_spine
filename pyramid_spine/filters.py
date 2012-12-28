import json
try:
    from markdown import markdown
except:
    def markdown(text, *args, **kwargs):
        return text

from pyramid.threadlocal import get_current_request

from pyramid_spine.utils import utc
def route_path_filter(route_name, *elements, **kw):
    request = get_current_request()
    return request.route_path(route_name, *elements, **kw)

def static_path_filter(path, **kw):
    request = get_current_request()
    return request.static_path(path, **kw)

def localtime(dt, assume=True):
    if dt is None:
        return dt
    request = get_current_request()
    tz = request.timezone
    if not dt.tzinfo:
        if assume:
            #assuming it's in UTC (THIS IS SO WRONG)
            dt = dt.replace(tzinfo=utc)
        else:
            return dt
    dt = dt.astimezone(tz)
    if hasattr(tz, 'normalize'):
        # available for pytz time zones
        dt = tz.normalize(dt)
    return dt

def strftime(dt, fmt):
    return dt.strftime(fmt)

def markdown_filter(text, *args, **kwargs):
    """
    Parse text with markdown library.

    :param text:   - text for parsing;
    :param args:   - markdown arguments (http://freewisdom.org/projects/python-markdown/Using_as_a_Module);
    :param kwargs: - markdown keyword arguments (http://freewisdom.org/projects/python-markdown/Using_as_a_Module);
    :return:       - parsed result.
    """
    return markdown(text, *args, **kwargs)

def jsonify(obj):
    return json.dumps(obj)
