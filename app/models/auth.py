from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from .. import db


DEPARTMENT = ["部门1", "部门2", "部门3"]


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    department = db.Column(db.String(128), unique=False)
    user_role = db.relationship("UserRole", backref="role")
    role_permission = db.relationship("RolePermission", backref="role")

    def __repr__(self):
        return "<Role {}>".format(self.name)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())


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
        super(User,self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    # def update_info(self, department_one=self.department_one, department_two=department_two, role_list=self.role_list, password):
    #     if self.department_one in DEPARTMENT.keys() and self.department_two in DEPARTMENT[self.department_one]:
    #         if set(role_list).issubset(set([role.name for role in Role.query.all()])):
    #
    #             self.password=password
    def update_user_role(self, role_list):

        return

    @property
    def role_list(self):
        return [user_role.role for user_role in self.user_role]

    @property
    def role_text(self):
        return ' '.join(["{}-{}".format(user_role.role.department, user_role.role.name) for user_role in self.user_role])

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


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.String(32), primary_key=True, default=str(uuid.uuid1()))
    name = db.Column(db.String(64), unique=True)
    need_granularity = db.Column(db.Boolean, default=False)
    granularities = db.relationship("Granularity", backref="permission")
    role_permission = db.relationship("RolePermission", backref="permission")

    def __repr__(self):
        return "<Permission {}>".format(self.name)

    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())


class Granularity(db.Model):
    __tablename__ = "granularities"
    id = db.Column(db.String(32), primary_key=True, default=str(uuid.uuid1()))
    name = db.Column(db.String(64), unique=True)
    permission_id = db.Column(db.String(32), db.ForeignKey("permissions.id"))

    def __repr__(self):
        return "<Granularity {}->{}>".format(self.permission, self.name)

    def __init__(self, **kwargs):
        super(Granularity, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())


class RolePermission(db.Model):
    __tablename__ = "role_permission"
    id = db.Column(db.String(32), primary_key=True, default=str(uuid.uuid1()))
    role_id = db.Column(db.String(32), db.ForeignKey("roles.id"))
    permission_id = db.Column(db.String(32), db.ForeignKey("permissions.id"))

    def __repr__(self):
        return "RolePermission {}<->{}".format(self.role, self.permission)

    def __init__(self, **kwargs):
        super(RolePermission, self).__init__(**kwargs)
        self.id = str(uuid.uuid1())
