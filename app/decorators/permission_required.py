# -*- coding: utf-8 -*-


from functools import wraps
from flask import session, abort
from app.models.users import User


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            current_user = User.get_user_by_email(session.get("email"))
            if not current_user.can(permission):
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator
