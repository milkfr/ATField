from app.models import BaseModel
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import CHAR
from sqlalchemy.orm import relationship


class Role(BaseModel):

    __tablename__ = 'auth_role'

    name = Column('uk_name', CHAR(36), nullable=False, unique=True)  # 角色名
    _users = relationship('User', secondary='auth_user_role', backref='roles')  # 多对多，用户
    _permissions = relationship('Permission', secondary='auth_role_permission', backref='roles')  # 多对多，权限

    _fields = ['uid', 'name', 'permissions']

    def _set_fields(self):
        self._fields = ['uid', 'name', 'permissions']

    def remove(self):
        self.users.clear()
        self.permissions.clear()
        super().remove()

    @classmethod
    def get_item_by_name(cls, name, status=1):
        return Role.query.filter(Role.status == status, Role.name == name).first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return Role.query.filter(Role.status == status, Role.uid == uid).first()

    @classmethod
    def list_items(cls, status=1):
        return Role.query.filter(Role.status == status).all()

    @classmethod
    def list_items_by_uids(cls, uids, status=1):
        return Role.query.filter(Role.status == status, Role.uid.in_(sorted(uids))).all()

    @classmethod
    def list_items_by_search(cls, uid, name, status=1):
        query = Role.query
        if uid:
            query = query.filter(Role.uid == uid)
        if name:
            query = query.filter(Role.name.ilike('%{}%'.format(name)))
        if status in [0, 1]:
            query = query.filter(Role.status == status)
        return query.all()

    def update_status(self):
        if self.status:
            self.remove()
        else:
            self.update(status=1)
