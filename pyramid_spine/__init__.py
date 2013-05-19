from pytz import timezone

def get_timezone(request):
    return timezone(request.registry.settings.get('timezone', 'UTC'))

