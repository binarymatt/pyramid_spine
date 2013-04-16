#from pyramid.threadlocal import get_current_registry
import uuid
from sqlalchemy import (
    Column,
    DateTime
)
from sqlalchemy.dialects import postgresql as postgres

from pyramid_spine.utils import utcnow

def hex_default():
    ud = uuid.uuid4().hex
    return ud

class UUIDPrimaryKeyMixin(object):
    id = Column(postgres.UUID(as_uuid=True), primary_key=True, default=hex_default)

class TimestampMixin(object):
    created_ts = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_ts = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)


