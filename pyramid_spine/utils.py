from datetime import datetime
import pytz
utc = pytz.utc
def utcnow():
    """
    Returns an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """
    return datetime.utcnow().replace(tzinfo=utc)

BASE2 = "01"
BASE10 = "0123456789"
BASE16 = "0123456789ABCDEF"
BASE62 = "AzByCxDwEvFuGtHsIrJqKpLoMnNmOlPkQjRiShTgUfVeWdXcYbZa0123456789"
def base62_to_int(number):
    return int(base_convert(number, BASE62, BASE10))

def int_to_base62(number):
    return base_convert(number, BASE10, BASE62)

def base_convert(number, fromradix, toradix):
    # based on http://code.activestate.com/recipes/111286/
    x = long(0)
    for digit in str(number):
        x = x * len(fromradix) + fromradix.index(digit)

    res = ""
    while x > 0:
        d = x % len(toradix)
        res = toradix[d] + res
        x /= len(toradix)

    return res
