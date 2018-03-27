#!/usr/bin/env python3

import os
import click

from app import create_app, db
from app.models.auth import User, Role, UserRole, Permission, RolePermission

from flask_script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
url_map = app.url_map
manager = Manager(app)  # 初始化插件


def make_shell_context():
    return dict(app=app, db=db,
                User=User, Role=Role, UserRole=UserRole,
                Permission=Permission, RolePermission=RolePermission)

manager.add_command("shell", Shell(make_context=make_shell_context))  # 添加命令行参数，补充上下文


@manager.command
def fake():
    from app.fake import generate_fake_auth
    db.drop_all()
    db.create_all()
    generate_fake_auth(url_map=url_map)


if __name__ == '__main__':
    manager.run()