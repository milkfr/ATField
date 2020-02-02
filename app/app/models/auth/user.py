from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import CHAR, TINYINT
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import BaseModel
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app
from app.libs.error_types import AuthFailedException


class User(BaseModel):

    __tablename__ = 'auth_user'

    name = Column('uk_name', CHAR(20), nullable=False, unique=True)  # 昵称
    password_hash = Column('password', CHAR(94))  # 加盐hash后的密码
    fail_count = Column(TINYINT(unsigned=True), default=0, nullable=False)  # 距上次登录成功后输错密码次数
    _roles = relationship('Role', secondary='auth_user_role', backref='users')  # 多对多，角色

    _fields = ['uid', 'name', 'roles']

    def _set_fields(self):
        self._fields = ['uid', 'name', 'roles']

    def can(self, permission):
        if len(set(self.roles) | set(permission.roles)) > 0:
            return True
        else:
            return False

    @property
    def password(self):
        return '**********'

    @password.setter
    def password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def verify_password(self, password):
        if self.fail_count >= 5:
            return False
        if check_password_hash(self.password_hash, password):
            self.update(fail_count=0)
            return True
        else:
            self.update(fail_count=self.fail_count+1)
        return False

    def generate_api_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'uid': self.uid}).decode('utf-8')

    @staticmethod
    def verify_api_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except BadSignature:
            raise AuthFailedException(msg='token is invalid')
        except SignatureExpired:
            raise AuthFailedException(msg='token is expired')
        return User.get_item_by_uid(data['uid'])

    def remove(self):
        self.roles.clear()
        super().remove()

    @classmethod
    def get_item_by_name(cls, name, status=1):
        return User.query.filter(User.status == status, User.name == name).first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return User.query.filter(User.status == status, User.uid == uid).first()

    @classmethod
    def list_items(cls, status=1):
        return User.query.filter(User.status == status).all()

    @classmethod
    def list_items_by_search(cls, uid, name, status=1):
        query = User.query
        if uid:
            query = query.filter(User.uid == uid)
        if name:
            query = query.filter(User.name.ilike('%{}%'.format(name)))
        if status in [0, 1]:
            query = query.filter(User.status == status)
        return query.all()
