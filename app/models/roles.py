# -*- coding: utf-8 -*-


from app import db


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.Integer)
    name = db.Column(db.String(64))
    users = db.relationship("User", backref="role", lazy="dynamic")
    roles_functions = db.relationship("RoleFunction", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role {}>".format(self.department + " " + self.name)

    @staticmethod
    def test_exist_role(name, department):
        if Role.query.filter_by(department=department, name=name).first() is None:
            return True
        return False

    @staticmethod
    def add_role_type(department, name):
        from sqlalchemy.exc import IntegrityError
        if Role.test_exist_role(department=department, name=name):
            role = Role(department=department, name=name)
            db.session.add(role)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def init_role_types():
        Role.add_role_type(department="user", name="default")
        Role.add_role_type(department="admin", name="root")

    @staticmethod
    def get_role_departments():
        return [roles.department for roles in Role.query.group_by(Role.department).all()]

    @staticmethod
    def get_role_by_id(id):
        return Role.query.filter_by(id=id).first()

    @staticmethod
    def update_role_by_id(id, department, name):
        from sqlalchemy.exc import IntegrityError
        if Role.test_exist_role(department=department, name=name):
            role = Role.query.filter_by(id=id).first()
            role.department = department
            role.name = name
            db.session.add(role)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def get_all_roles():
        return [(roles.department, roles.name) for roles in Role.query.order_by(Role.department).all()]

    @staticmethod
    def delete_role_by_id(id):
        role = Role.query.filter_by(id=id).first()
        db.session.delete(role)
        db.session.commit()
