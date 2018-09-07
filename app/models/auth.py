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

    def update_permission_by_id(self, delete_permission_list, add_permission_list):
        for permission_id in delete_permission_list:
            rp = RolePermission.query.filter(RolePermission.role == self,
                                             RolePermission.permission_id == permission_id).first()
            db.session.delete(rp)
        for permission_id in add_permission_list:
            rp = RolePermission(role=self, permission_id=permission_id)
            db.session.add(rp)
        db.session.commit()

    @property
    def permission_list(self):
        return [role_permission.permission for role_permission in self.role_permission]

    @staticmethod
    def insert_items(role_info_list):
        # role_info_list = [{"name": None, "department": None}, {...}]
        for role_info in role_info_list:
            role = Role(name=role_info["name"], department=role_info["department"])
            db.session.add(role)
        db.session.commit()

    def delete_item(self):
        for ur in UserRole.query.filter(UserRole.role == self).all():
            db.session.delete(ur)
        for rp in RolePermission.query.filter(RolePermission.role == self).all():
            db.session.delete(rp)
        db.session.delete(self)
        db.session.commit()


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

    def update_role_by_id(self, delete_role_list, add_role_list):
        for role_id in delete_role_list:
            ur = UserRole.query.filter(UserRole.user == self, UserRole.role_id == role_id).first()
            db.session.delete(ur)
        for role_id in add_role_list:
            ur = UserRole(user=self, role_id=role_id)
            db.session.add(ur)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def role_list(self):
        return [user_role.role for user_role in self.user_role]

    @staticmethod
    def insert_items(user_info_list):
        # user_info_list = [{"name": None, "department": None, "password": "None"}, {...}]
        for user_info in user_info_list:
            user = User(name=user_info["name"], department=user_info["department"], password=user_info["password"])
            db.session.add(user)
        db.session.commit()

    def delete_item(self):
        for ur in UserRole.query.filter(UserRole.user == self).all():
            db.session.delete(ur)
        db.session.delete(self)
        db.session.commit()


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

    @staticmethod
    def get_models():
        # 显示所有权限分类
        data = {}
        for item in Permission.query.all():
            data[item.endpoint.split('.')[0]] = []
        for item in Permission.query.all():
            data[item.endpoint.split('.')[0]].append(item)
        return data

    @staticmethod
    def insert_items(permission_info_list):
        # permission_info_list = [{"name": None, "endpoint": None}, {...}]
        for permission_info in permission_info_list:
            permission = Permission(name=permission_info["name"], endpoint=permission_info["endpoint"])
            db.session.add(permission)
        db.session.commit()

    def delete_item(self):
        for rp in RolePermission.query.filter(RolePermission.permission == self).all():
            db.session.delete(rp)
        db.session.delete(self)
        db.session.commit()


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
