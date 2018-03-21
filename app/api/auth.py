from flask import render_template
from ..models.auth import User

from . import api


@api.route("/user", defaults={"page": 1, "per_page": 5, "key": ""})
@api.route("/user/<int:page>/<int:per_page>/<path:key>")
def user(page=1, per_page=5, key=''):
    theaders = ["id", "用户名", "角色"]
    pagination = User.query.order_by(User.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    tbodys = []
    for user in pagination.items:
        item = []
        item.append(user.id)
        item.append(user.name)
        item.append(' '.join([user_role.role.name for user_role in user.user_role]))
    return render_template('auth/user.html', theaders=theaders, pagination=pagination, url='main.test')
