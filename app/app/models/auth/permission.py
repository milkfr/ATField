from app.models import BaseModel
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql.types import VARCHAR


class Permission(BaseModel):

    __tablename__ = 'auth_permission'

    endpoint = Column('uk_endpoint', VARCHAR(50), nullable=False, unique=True)  # flask endpoint
    _roles = relationship('Role', secondary='auth_role_permission', backref='permissions')  # 多对多，角色

    _fields = ['uid', 'endpoint']

    def _set_fields(self):
        self._fields = ['uid', 'endpoint']

    def remove(self):
        self.roles.clear()
        super().remove()

    @classmethod
    def list_items(cls, status=1):
        return Permission.query.filter(Permission.status == status).all()

    @classmethod
    def get_item_by_endpoint(cls, endpoint=None, status=1):
        return Permission.query.filter(Permission.status == status, Permission.endpoint == endpoint).first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return Permission.query.filter(Permission.status == status, Permission.uid == uid).first()

    @classmethod
    def list_items_by_uids(cls, uids, status=1):
        return Permission.query.filter(Permission.status == status, Permission.uid.in_(sorted(uids))).all()

    @classmethod
    def list_items_by_search(cls, uid, endpoint, status=1):
        query = Permission.query
        if uid:
            query = query.filter(Permission.uid == uid)
        if endpoint:
            query = query.filter(Permission.endpoint.ilike('%{}%'.format(endpoint)))
        if status in [0, 1]:
            query = query.filter(Permission.status == status)
        return query.all()
