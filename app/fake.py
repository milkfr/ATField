from random import randint
from faker import Faker
from sqlalchemy.exc import IntegrityError
from . import db
from .models.auth import User, Role, UserRole, Permission, Granularity, RolePermission


def _generate_fake_role(count=20):
    fake = Faker()
    for i in range(count):
        r = Role(name=fake.word())
        db.session.add(r)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def _generate_fake_user(count=100):
    fake = Faker()
    for i in range(count):
        u = User(name=fake.email(),
                 password="password")
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def _generate_fake_permission(count=20):
    fake = Faker()
    for i in range(count):
        p = Permission(name=fake.word())
        db.session.add(p)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def _generate_fake_granulatiry(count=20):
    fake = Faker()
    for i in range(count):
        g = Granularity(name=fake.word(),
                 permission=Permission.query.offset(randint(0, Permission.query.count()-1)).first())
        db.session.add(g)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def generate_fake_auth(permission_count=20, granularity_count=20, user_count=100, role_count=20):
    _generate_fake_permission(permission_count)
    _generate_fake_granulatiry(granularity_count)
    _generate_fake_role(role_count)
    _generate_fake_user(user_count)
    for j in range(User.query.count()):
        for i in range(Role.query.count()):
            if randint(0, 5) is 0:
                ur = UserRole(user=User.query.offset(j).first(), role=Role.query.offset(i).first())
                db.session.add(ur)
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
    for i in range(Permission.query.count()):
        for j in range(Role.query.count()):
            if randint(0, 5) is 0:
                rp = RolePermission(permission=Permission.query.offset(i).first(), role=Role.query.offset(j).first())
                db.session.add(rp)
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
