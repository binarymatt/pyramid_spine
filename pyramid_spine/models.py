from pyramid.threadlocal import get_current_registry
from pyramid.security import unauthenticated_userid
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension
from cryptacular.pbkdf2 import PBKDF2PasswordManager
hasher = PBKDF2PasswordManager()

from pyramid_spine.utils import utcnow

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
class Base(object):
    """Base class which provides automated table name
    and surrogate primary key column.

    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base)
Base.query = DBSession.query_property()


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

def authenticate_user(username, password):
    registry = get_current_registry()
    User = user_factory(registry)
    return False

def user_factory(registry):
    klass = getattr(registry, 'spine_auth_class')
    if not klass:
        raise NotImplementedError('You need to add spine_auth_class to your registry.')
    return klass

def get_user(request):
    # the below line is just an example, use your own method of
    # accessing a database connection here (this could even be another
    # request property such as request.db, implemented using this same
    # pattern).
    User = user_factory(request.registry)
    userid = unauthenticated_userid(request)
    if userid is not None:
        # this should return None if the user doesn't exist
        # in the database
        return User.query.filter_by(id=userid).first()

class TimestampMixin(object):
    created_ts = Column(DateTime(timezone=True), default=utcnow)
    updated_ts = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

class UserMixin(TimestampMixin):
    __tablename__ = 'users'
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def check_password(self, raw_password):
        return hasher.check(self.password, raw_password)

    def set_password(self, password):
        self.password = hasher.encode(password)

