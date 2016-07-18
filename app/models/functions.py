# -*- coding: utf-8 -*-


from app import db


class Function(db.Model):
    __tablename__ = "functions"
    id = db.Column(db.Integer, primary_key=True)
    part = db.Column(db.String(64))
    name = db.Column(db.String(64))
    permission = db.Column(db.String(64), unique=True)
    publish = db.Column(db.Boolean, default=False)
    roles_functions = db.relationship("RoleFunction", backref="function", lazy="dynamic")

    def __repr__(self):
        return "<Function {}>".format(self.department + ' ' + self.name)

    @staticmethod
    def xor_function(permission):
        function = Function.get_function_by_permission(permission)
        function.publish = not function.publish
        db.session.add(function)
        db.session.commit()

    @staticmethod
    def get_all_function():
        return Function.query.all()

    @staticmethod
    def get_published_function():
        return Function.query.filter_by(publish=True).order_by(Function.name).all()

    @staticmethod
    def get_function_by_permission(permission):
        return Function.query.filter_by(permission=permission).first()

    @staticmethod
    def get_function_by_type(part, name):
        return Function.query.filter_by(part=part, name=name).first()

    @staticmethod
    def test_exist_function(part, name, permission):
        if Function.get_function_by_type(part=part, name=name) is None \
                or Function.get_function_by_permission(permission=permission) is None:
            return True
        return False

    @staticmethod
    def add_function_type(part, name, permission):
        from sqlalchemy.exc import IntegrityError
        if Function.test_exist_function(part, name, permission):
            function = Function(part=part, name=name, permission=permission)
            db.session.add(function)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def update_function_by_permission(permission, part, name):
        from sqlalchemy.exc import IntegrityError
        function = Function.get_function_by_permission(permission=permission)
        function.part = part
        function.name = name
        db.session.add(function)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    @staticmethod
    def delete_function_by_permission(permission):
        function = Function.get_function_by_permission(permission=permission)
        db.session.delete(function)
        db.session.commit()

    @staticmethod
    def init_function_type():
        Function.add_function_type(part="user", name="base", permission="USER_BASE")
        Function.add_function_type(part="admin", name="base", permission="ADMIN_BASE")
        Function.add_function_type(part="document", name="base", permission="DOCUMENT_BASE")

