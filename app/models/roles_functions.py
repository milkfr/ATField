# -*- coding: utf-8 -*-


from app import db


class RoleFunction(db.Model):
    __tablename__ = "roles_functions"
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    function_id = db.Column(db.Integer, db.ForeignKey("functions.id"))