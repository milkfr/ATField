# -*- coding: utf-8 -*-


from app import db


class RoleFunction(db.Model):
    __tablename__ = "roles_functions"
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    function_id = db.Column(db.Integer, db.ForeignKey("functions.id"))

    @staticmethod
    def get_function_by_role_id(id):
        tmp = RoleFunction.query.filter_by(role_id=id).all()
        function = []
        for i in tmp:
            tmp_data = {
                "role_function_id": i.id,
                "function_id": i.function_id,
                "function_part": i.function.part,
                "function_name": i.function.name
            }
            function.append(tmp_data)
        return function

    @staticmethod
    def delete_by_id(id):
        role = RoleFunction.query.filter_by(id=id).first()
        db.session.delete(role)
        db.session.commit()

    @staticmethod
    def get_role_function_by_all_id(role_id, function_id):
        return RoleFunction.query.filter_by(role_id=role_id, function_id=function_id).first()

    @staticmethod
    def add_by_role_function_id(role_id, function_id):
        role_function = RoleFunction(role_id=role_id, function_id=function_id)
        db.session.add(role_function)
        db.session.commit()

