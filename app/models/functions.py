# -*- coding: utf-8 -*-


from app import db


class Function(db.Model):
    __tablename__ = "functions"
    id = db.Column(db.Integer, primary_key=True)
    part = db.Column(db.String(64))
    name = db.Column(db.String(64))
    permission = db.Column(db.String(64), unique=True)
    roles_functions = db.relationship("RoleFunction", backref="function", lazy="dynamic")

    def __repr__(self):
        return "<Function {}>".format(self.department + ' ' + self.name)

    @staticmethod
    def get_function_by_permission(permission):
        return Function.query.filter_by(permission=permission).first()

    @staticmethod
    def get_function_by_type(part, name):
        return Function.query.filter_by(part=part, name=name).first()

    @staticmethod
    def test_exist_function(part, name, permission):
        if Function.query.filter_by(part=part, name=name).first() is None \
                or Function.query.filter_by(permission=permission).first() is None:
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
        function = Function.query.filter_by(permission=permission).first()
        function.part = part
        function.name = name
        db.session.add(function)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    @staticmethod
    def delete_function_by_permission(permission):
        function = Function.query.filter_by(permission=permission).first()
        db.session.delete(function)
        db.session.commit()
