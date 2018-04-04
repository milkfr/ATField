#!/usr/bin/env python3

import os
import click

from app import create_app, db
from app.models.auth import User, Role, UserRole, Permission, RolePermission, Granularity

from flask_script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
url_map = app.url_map
manager = Manager(app)  # 初始化插件


def make_shell_context():
    return dict(app=app, db=db,
                User=User, Role=Role, UserRole=UserRole,
                Permission=Permission, RolePermission=RolePermission, Granularity=Granularity)

manager.add_command("shell", Shell(make_context=make_shell_context))  # 添加命令行参数，补充上下文


@manager.command
def fake():
    from app.fake import generate_fake_auth
    db.drop_all()
    db.create_all()
    # Add user
    u1 = User(name="aaa", department="部门1", password="123456")
    u2 = User(name="bbb", department="部门2", password="123456")
    u3 = User(name="ccc", department="部门1", password="123456")
    db.session.add_all([u1, u2, u3])
    r1 = Role(name="role1", department="部门1")
    r2 = Role(name="role2", department="部门2")
    r3 = Role(name="admin", department="特权")
    db.session.add_all([r1, r2, r3])
    ur1 = UserRole(user=u1, role=r1)
    ur2 = UserRole(user=u1, role=r3)
    ur3 = UserRole(user=u2, role=r2)
    ur4 = UserRole(user=u3, role=r1)
    db.session.add_all([ur1, ur2, ur3, ur4])
    p1 = Permission(name="用户列表查看", endpoint="auth.user_list")
    p2 = Permission(name="用户角色设定", endpoint="auth.user_update")
    p3 = Permission(name="角色列表查看", endpoint="auth.role_list")
    p4 = Permission(name="角色权限设定", endpoint="auth.role_update")
    p5 = Permission(name="权限列表查看", endpoint="auth.permission_list")
    db.session.add_all([p1, p2, p3, p4, p5])
    rp1 = RolePermission(role=r3, permission=p1)
    rp2 = RolePermission(role=r3, permission=p2)
    rp3 = RolePermission(role=r3, permission=p3)
    rp4 = RolePermission(role=r3, permission=p4)
    rp5 = RolePermission(role=r3, permission=p5)
    rp6 = RolePermission(role=r2, permission=p1)
    rp7 = RolePermission(role=r1, permission=p3)
    db.session.add_all([rp1, rp2, rp3, rp4, rp5, rp6, rp7])
    db.session.commit()

    # generate_fake_auth(url_map=url_map)


if __name__ == '__main__':
    manager.run()