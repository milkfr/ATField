#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from flask_script import Manager, Shell
from app import create_app, db
from app.models.users import User
from app.models.roles import Role
from app.models.functions import Function
from app.models.roles_functions import RoleFunction
from app.models.documents import Document


app = create_app(os.getenv("FLASK_CONFIG") or "default")

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, RoleFunction=RoleFunction, Role=Role, Function=Function, Document=Document)

manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
