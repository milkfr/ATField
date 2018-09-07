from flask import render_template, request, url_for, redirect
from ..models.auth import User, Role, Permission

from . import auth
from .forms import UserUpdateForm, RoleUpdateForm


@auth.route("/user/list", methods=["GET"])
def user_list():
    # 获取用户列表
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = User.query.filter(User.name.ilike('%'+key+'%')).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("auth/user_list.html", pagination=pagination, url='auth.user_list')


@auth.route("/user/update", methods=["GET", "POST"])
def user_update():
    # 用户角色信息设定
    user_id = request.args.get("id", "", type=str)
    user = User.query.filter(User.id == user_id).first()
    form = UserUpdateForm(user)
    if form.validate_on_submit():
        role_id_list = form.role.data
        old_role_id_list = [user_role.role.id for user_role in user.user_role]
        # 删掉user已有但新增没有的差集
        delete_role_list = list(set(old_role_id_list).difference(set(role_id_list)))
        # 新增已有但user没有差集
        add_role_list = list(set(role_id_list).difference(set(old_role_id_list)))
        user.update_role_by_id(delete_role_list, add_role_list)
        return redirect(url_for("auth.user_list"))
    form.name.data = user.name
    form.department.data = user.department
    form.role.data = [role.id for role in user.role_list]
    return render_template("auth/user_update.html", form=form)


@auth.route("/role/list", methods=["GET"])
def role_list():
    # 角色列表
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Role.query.filter(Role.name.ilike('%'+key+'%')).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("auth/role_list.html", pagination=pagination, url='auth.role_list')


@auth.route("/role/update", methods=["GET", "POST"])
def role_update():
    # 角色权限信息设定
    role_id = request.args.get("id", '', type=str)
    role = Role.query.filter(Role.id == role_id).first()
    form = RoleUpdateForm()
    if request.method == "POST":
        permission_id_list = form.permission.data
        old_permission_id_list = [permission.id for permission in role.permission_list]
        # 删掉role已有但新增没有的差集
        delete_permission_list = list(set(old_permission_id_list).difference(set(permission_id_list)))
        # 新增已有但user没有的差集
        add_permission_list = list(set(permission_id_list).difference(set(old_permission_id_list)))
        role.update_permission_by_id(delete_permission_list, add_permission_list)
        return redirect(url_for("auth.role_list"))
    return render_template("auth/role_update.html", role=role, Permission=Permission)


@auth.route("/permission/list", methods=["GET"])
def permission_list():
    # 获取权限列表
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "", type=str)
    pagination = Permission.query.filter(Permission.name.ilike('%'+key+'%')).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("auth/permission_list.html", pagination=pagination, url="auth.permission_list")
