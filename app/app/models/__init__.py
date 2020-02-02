from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery, Pagination as _Pagination
from sqlalchemy import Column, orm, types
from sqlalchemy.dialects.mysql.base import MSBinary
from sqlalchemy.dialects.mysql.types import DATETIME, TINYINT
from contextlib import contextmanager

from app.libs.error_types import NotFoundException


class MixinJSONSerializer:

    _fields = []  # Some errors will occur in unit tests without this line

    @orm.reconstructor
    def init_on_load(self):
        self._fields = []
        self._set_fields()

    def _set_fields(self):
        pass

    def hide(self, *args):
        for key in args:
            self._fields.remove(key)

    def append(self, *args):
        for key in args:
            self._fields.append(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, item):
        return getattr(self, item)


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self, commit=True):
        try:
            yield
            if commit:
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Pagination(_Pagination):

    def keys(self):
        return ['total', 'items', 'per_page', 'page']

    def __getitem__(self, item):
        return getattr(self, item)


class Query(BaseQuery):

    def paginate(self, page=None, per_page=None, error_out=True, max_per_page=None):
        """paginate json serializer"""
        pagination = super().paginate(page=page, per_page=per_page, error_out=error_out, max_per_page=max_per_page)
        return Pagination(self, pagination.page, pagination.per_page, pagination.total, pagination.items)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFoundException()
        return rv

    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFoundException()
        return rv


db = SQLAlchemy(query_class=Query)


class UUID(types.TypeDecorator):
    """MySQL UUID type"""

    impl = MSBinary

    def __init__(self):
        self.impl.length = 16
        types.TypeDecorator.__init__(self, length=self.impl.length)

    def process_bind_param(self, value, dialect):
        if value and isinstance(value, uuid.UUID):
            return value.bytes
        elif value and isinstance(value, str):
            return uuid.UUID(value).bytes
        elif value:
            raise ValueError('value %s is not a type uuid.UUID'.format(value))
        else:
            return None

    def process_result_value(self, value, dialect):
        if value:
            return str(uuid.UUID(bytes=value))
        else:
            return None

    def is_mutable(self):
        return False


class BaseModel(db.Model, MixinJSONSerializer):
    __abstract__ = True
    uid = Column(UUID, primary_key=True, nullable=False)
    utc_created = Column(DATETIME, nullable=False)
    utc_modified = Column(DATETIME, nullable=False)
    status = Column(TINYINT(unsigned=True), default=1, nullable=False)

    def __init__(self):
        self.uid = uuid.uuid1()
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.utc_created = now
        self.utc_modified = now

    @classmethod
    def save(cls, **kwargs):
        one = cls()
        for key in kwargs.keys():
            if hasattr(one, key):
                setattr(one, key, kwargs[key])
        db.session.add(one)
        return one

    def update(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
        self.utc_modified = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(self)

    def remove(self):
        self.update(status=0)

    def activate(self):
        self.update(status=1)
