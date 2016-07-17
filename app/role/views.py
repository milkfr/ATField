# -*- coding: utf-8 -*-


from flask import render_template, redirect, url_for

from app.role.forms import RoleForm
from app.role import role
from app.decorators.login_required import login_required
from app.models.roles import Role


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
        if Role.test_exist_role(department=department, name=name) is None:
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
        if Role.test_exist_role(department=department, name=name) is None:
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




