# -*- coding: utf-8 -*-


from flask import render_template, redirect, url_for

from app.role.forms import RoleForm, FunctionAddForm
from app.role import role
from app.decorators.login_required import login_required
from app.models.roles import Role
from app.models.roles_functions import RoleFunction


@role.route("/")
@login_required
def home():
    headings = ["id", "department", "name"]
    contents = Role.query.order_by(Role.department).all()
    return render_template("role/home.html", headings=headings, contents=contents)


@role.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = RoleForm()
    if form.validate_on_submit():
        department = form.department.data
        name = form.name.data
        if Role.test_exist_role(department=department, name=name):
            Role.add_role_type(department=department, name=name)
            return redirect(url_for("role.home"))
    return render_template("role/edit.html", form=form)


@role.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    form = RoleForm()
    if form.validate_on_submit():
        department = form.department.data
        name = form.name.data
        if Role.test_exist_role(department=department, name=name):
            Role.update_role_by_id(id=id, department=department, name=name)
            return redirect(url_for("role.home"))
    tmp_role = Role.get_role_by_id(id)
    form.department.data = tmp_role.department
    form.name.data = tmp_role.name
    return render_template("role/edit.html", form=form)


@role.route("/delete/<int:id>")
@login_required
def delete(id):
    Role.delete_role_by_id(id)
    return redirect(url_for("role.home"))


@role.route("/function/<int:id>", methods=["GET", "POST"])
@login_required
def function(id):
    form = FunctionAddForm(role_id=id)
    if form.validate_on_submit():
        RoleFunction.add_by_role_function_id(role_id=id, function_id=form.function.data)
    contents = RoleFunction.get_function_by_role_id(id)
    headings = ["role_function_id", "function_id", "function_part", "function_name"]
    return render_template("role/function.html", role_id=id, contents=contents, headings=headings, form=form)


@role.route("/function/<int:id>/delete/<int:role_function_id>")
@login_required
def function_delete(id, role_function_id):
    RoleFunction.delete_by_id(role_function_id)
    return redirect(url_for("role.function", id=id))
