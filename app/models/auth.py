from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from .. import db


DEPARTMENT = ["部门1", "部门2", "部门3"]


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    department = db.Column(db.String(128), unique=False)
    user_role = db.relationship("UserRole", backref="role")
    role_permission = db.relationship("RolePermission", backref="role")

    def __repr__(self):
        return "<{}-{}>".format(self.department, self.name)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    def delete_permission(self, permission):
        rp = RolePermission.query.filter(RolePermission.role == self, RolePermission.permission == permission).first()
        db.session.delete(rp)
        db.session.commit()

    def add_permission(self, permission):
        rp = RolePermission(role=self, permission=permission)
        db.session.add(rp)
        db.session.commit()

    @property
    def permission_list(self):
        return [role_permission.permission for role_permission in self.role_permission]


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    department = db.Column(db.String(128), unique=False)
    user_role = db.relationship("UserRole", backref="user")

    def __repr__(self):
        return "<User {}>".format(self.name)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    def can(self, permission):
        permissions = []
        for role in self.role_list:
            permissions.extend(role.permission_list)
        if permission in permissions:
            return True
        return False

    def delete_role(self, role):
        ur = UserRole.query.filter(UserRole.user == self, UserRole.role == role).first()
        db.session.delete(ur)
        db.session.commit()

    def add_role(self, role):
        if role.department != "特权" and role.department != self.department:
            return
        else:
            ur = UserRole(user=self, role=role)
            db.session.add(ur)
            db.session.commit()

    @property
    def role_list(self):
        return [user_role.role for user_role in self.user_role]

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.String(32), primary_key=True)
    role_id = db.Column(db.String(32), db.ForeignKey("roles.id"))
    user_id = db.Column(db.String(32), db.ForeignKey("users.id"))

    def __repr__(self):
        return "<UserRole {}<->{}>".format(self.user, self.role)

    def __init__(self, **kwargs):
        super(UserRole, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    @staticmethod
    def delete_relationship_by_role(role):
        for ur in UserRole.query.filter(UserRole.role == role).all():
            db.session.delete(ur)
        db.session.commit()

    @staticmethod
    def delete_relationship_by_user(user):
        for ur in UserRole.query.filter(UserRole.user == user).all():
            db.session.delete(ur)
        db.session.commit()


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    endpoint = db.Column(db.String(128), unique=True)
    role_permission = db.relationship("RolePermission", backref="permission")

    def __repr__(self):
        return "<{}-{}>".format(self.name, self.endpoint)

    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    @classmethod
    def get_models(cls):
        # 显示所有权限分类
        data = {}
        for item in Permission.query.all():
            data[item.endpoint.split('.')[0]] = []
        for item in Permission.query.all():
            data[item.endpoint.split('.')[0]].append(item)
        return data


class RolePermission(db.Model):
    __tablename__ = "role_permission"
    id = db.Column(db.String(32), primary_key=True)
    role_id = db.Column(db.String(32), db.ForeignKey("roles.id"))
    permission_id = db.Column(db.String(32), db.ForeignKey("permissions.id"))

    def __repr__(self):
        return "RolePermission {}<->{}".format(self.role, self.permission)

    def __init__(self, **kwargs):
        super(RolePermission, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    @staticmethod
    def delete_relationship_by_role(role):
        for rp in RolePermission.query.filter(RolePermission.role == role).all():
            db.session.delete(rp)
        db.session.commit()

    @staticmethod
    def delete_relationship_by_permission(permission):
        for rp in RolePermission.query.filter(RolePermission.permission == permission).all():
            db.session.delete(rp)
        db.session.commit()
