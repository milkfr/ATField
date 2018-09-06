from random import randint, choice
from faker import Faker
from sqlalchemy.exc import IntegrityError
from . import db
from .models.auth import User, Role, UserRole, Permission, RolePermission, DEPARTMENT


def _generate_fake_role(count=20):
    fake = Faker()
    for i in range(count):
        r = Role(name=fake.word(), department=choice(DEPARTMENT))
        db.session.add(r)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    for i in range(5):
        r = Role(name=fake.word(), department="特权")
        db.session.add(r)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def _generate_fake_user(count=100):
    fake = Faker()
    for i in range(count):
        u = User(name=fake.email(), department=choice(DEPARTMENT), password="password")
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def _generate_fake_permission(count=20, url_map=None):
    fake = Faker()
    for item in url_map.iter_rules():
        p = Permission(name=fake.word(), endpoint=item.endpoint)
        db.session.add(p)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def generate_fake_auth(permission_count=20, user_count=100, role_count=20, url_map=None):
    _generate_fake_permission(permission_count, url_map=url_map)
    _generate_fake_role(role_count)
    _generate_fake_user(user_count)
    # generate fake user role relationship
    for j in range(User.query.count()):
        for i in range(Role.query.count()):
            if randint(0, 2) is 0:
                User.query.offset(j).first().add_role(role=Role.query.offset(i).first())
    # generate fake role permission relationship
    for i in range(Permission.query.count()):
        for j in range(Role.query.count()):
            if randint(0, 5) is 0:
                Role.query.offset(j).first().add_permission(permission=Permission.query.offset(i).first())
                # rp = RolePermission(permission=Permission.query.offset(i).first(), role=Role.query.offset(j).first())
                # db.session.add(rp)
                # try:
                #     db.session.commit()
                # except IntegrityError:
                #     db.session.rollback()
