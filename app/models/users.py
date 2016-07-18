# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from .. import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User {}>".format(self.email)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def add_new_user(email, password):
        from sqlalchemy.exc import IntegrityError
        user = User(email=email, password=password, role_id=1)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def can(self, permission):
        from app.models.functions import Function
        from app.models.roles_functions import RoleFunction
        function = Function.get_function_by_permission(permission=permission)
        if RoleFunction.get_role_function_by_all_id(role_id=self.role.id, function_id=function.id) is not None:
            return True
        return False

    def is_admin(self):
        return self.can("ADMIN_BASE")

    def is_document(self):
        return self.can("DOCUMENT_BASE")

    def is_user(self):
        return self.can("USER_BASE")

    def bind_role_by_role_id(self, role_id):
        self.role_id = role_id
        db.session.add(self)
        db.session.commit()

    def get_permission_for_browser(self):
        from app.models.functions import Function
        role_functions = self.role.roles_functions
        permission = []
        for i in role_functions:
            tmp = Function.query.filter_by(id=i.function_id).first().permission
            permission.append(tmp)
        return permission

    @staticmethod
    def generate_fake(count=100):
        import forgery_py
        from app.models.roles import Role
        Role.init_role_types()
        from app.models.functions import Function
        Function.init_function_type()
        from app.models.roles_functions import RoleFunction
        role_function_1 = RoleFunction(role_id=1, function_id=1)
        role_function_2 = RoleFunction(role_id=2, function_id=1)
        role_function_3 = RoleFunction(role_id=2, function_id=2)
        role_function_4 = RoleFunction(role_id=2, function_id=3)
        role_function_5 = RoleFunction(role_id=3, function_id=3)
        db.session.add(role_function_1)
        db.session.add(role_function_2)
        db.session.add(role_function_3)
        db.session.add(role_function_4)
        db.session.add(role_function_5)
        db.session.commit()
        from random import seed
        seed()
        for i in range(count):
            User.add_new_user(email=forgery_py.internet.email_address(),
                              password=forgery_py.lorem_ipsum.word())
        User.add_new_user(email='291509722@qq.com', password='1')
