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

    @staticmethod
    def generate_fake(count=100):
        import forgery_py
        from random import seed
        seed()
        for i in range(count):
            User.add_new_user(email=forgery_py.internet.email_address(),
                              password=forgery_py.lorem_ipsum.word())
