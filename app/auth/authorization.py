from flask import render_template, request
from ..models.auth import User

from . import auth

### 用户管理
# 用户详情


@auth.route("/user", methods=["GET"])
def user():
    # 获取用户列表
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = User.query.filter(User.name.ilike('%'+key+'%')).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("auth/user.html", pagination=pagination, url='auth.user')


# @auth.route("/user/update", methods=["GET", "POST"])
# def user_update():
    # 用户信息设定


### 角色管理
# 新增角色
# 删除角色
# 角色权限设定

### 权限管理
#