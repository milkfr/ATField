from functools import wraps
from flask import session, redirect, url_for, abort


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("email", None):
            return redirect(url_for("auth.index"))
        return func(*args, **kwargs)
    return wrapper


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorator_function(*args, **kwargs):
            abort(403)
            return func(*args, **kwargs)
        return decorator_function
    return decorator