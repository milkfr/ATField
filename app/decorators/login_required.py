# -*- coding: utf-8 -*-


from functools import wraps
from flask import session, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("email", None):
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper
