from functools import wraps
from flask import session, abort
from app.models.auth import User


def permission_middleware():
    permission = request.get.user_permissions()
    if '{}-{}'.format(handler.__class__, handler.func_name) not in permissions:
        abort(403)

def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            current_user = User.query.filter(User.name=session.get("name"))
            if not current_user.can(permission):
                abort(403)
            return function(*args, **kwargs)
        return decorated_function
    return decorator


"""
object_id_list = request.user.permissions.get_object_id_list()
if need_limit_object and model == request.user.permissions.get_model:
       sql = ‘select * from model where id in {}’.format(tuple(object_id_list))
       return fetch_data(sql)
"""