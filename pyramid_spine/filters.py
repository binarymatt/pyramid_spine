from pyramid.threadlocal import get_current_request

def route_path_filter(route_name, *elements, **kw):
    request = get_current_request()
    return request.route_path(route_name, *elements, **kw)

def static_path_filter(path, **kw):
    request = get_current_request()
    return request.static_path(path, **kw)
