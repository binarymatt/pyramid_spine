from datetime import datetime
import pytz
utc = pytz.utc
def utcnow():
    """
    Returns an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """
    return datetime.utcnow().replace(tzinfo=utc)
