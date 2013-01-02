import hashlib
import hmac
import time
from pyramid.util import strings_differ

from pyramid_spine.utils import int_to_base62, base62_to_int

class TokenGenerator(object):
    """
    general algorithm was borrowed from djangos password reset token generator
    """
    def create_token(self, user, key=None):
        #timestamp is number to seconds since epoch
        ts = int(time.time())
        return self._make_token(user, ts, key)

    def _make_token(self, user, ts, key=None):
        ts_b62 = int_to_base62(ts)
        if key is None:
            key = 'pyramid_spint.tokens.TokenGenerator'
        value = (unicode(user.id) + user.password + unicode(ts))
        hash = hmac.new(key, value, digestmod=hashlib.sha1).hexdigest()
        return '%s-%s' % (ts_b62, hash)

    def check_token(self, user, token, limit=86400):
        try:
            ts_b62, hash = token.split("-")
        except ValueError:
            return False

        try:
            ts = base62_to_int(ts_b62)
        except ValueError:
            return False

        if strings_differ(self._make_token(user, ts), token):
            return False
        if limit:
            now = int(time.time())
            if now > ts + int(limit):
                return False

        return True

token_generator = TokenGenerator()

