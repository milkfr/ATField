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
        rp = RolePermission.query.filter_by(role=self, permission=permission).first()
        db.session.delete(ur)
        db.session.commit()

    def add_permission(self, permission):
        if permission != "特权" and permission.department != self.department:
            return
        else:
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
        super(User,self).__init__(**kwargs)
        self.id = str(uuid.uuid1())

    def delete_role(self, role):
        ur = UserRole.query.filter_by(user=self, role=role).first()
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


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.String(32), primary_key=True, default=str(uuid.uuid1()))
    name = db.Column(db.String(64), unique=True)
    department = db.Column(db.String(128), unique=False)
    need_granularity = db.Column(db.Boolean, default=False)
    granularities = db.relationship("Granularity", backref="permission")
    role_permission = db.relationship("RolePermission", backref="permission")

    def __repr__(self):
        return "<{}-{}>".format(self.department, self.name)

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
