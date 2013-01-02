import unittest
import time
from pyramid_spine.tokens import TokenGenerator

class TokenTests(unittest.TestCase):
    def test_create_token(self):
        """
        a valid token is created and checked
        """
        User = type('User', (), {})
        user = User()
        user.id = 1
        user.password = 'pass'
        t0 = TokenGenerator()
        tk = t0.create_token(user)
        self.assertTrue(t0.check_token(user, tk))

    def test_timeout(self):
        """
        testing to make sure that a token is invalid after the set amount of time
        """
        User = type('User', (), {})
        user = User()
        user.id = 1
        user.password = 'pass'
        t0 = TokenGenerator()
        ts = int(time.time()) - 86401
        tk = t0._make_token(user, ts)
        self.assertFalse(t0.check_token(user, tk))
