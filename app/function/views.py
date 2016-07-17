# -*- coding: utf-8 -*-


from flask import render_template, redirect, url_for

from app.function.forms import FunctionForm
from app.function import function
from app.decorators.login_required import login_required
from app.models.functions import Function


@function.route("/")
@login_required
def home():
    headings = ["part", "name", "permission"]
    contents = Function.query.order_by(Function.part).all()
    return render_template("function/home.html", headings=headings, contents=contents)


@function.route("/new", methods=["GET", "POST"])
@login_required
def new():
   form = FunctionForm()
   if form.validate_on_submit():
       part = form.part.data
       name= form.part.data
       permission = form.permission.data
       if Function.test_exist_function(part=part, name=name, permission=permission):
           Function.add_function_type(part=part, name=name, permission=permission)
           return redirect(url_for("function.home"))
   return render_template("function/edit.html", form=form)


@function.route("/edit/<permission>", methods=["GET", "POST"])
def edit(permission):
    form = FunctionForm()
    if form.validate_on_submit():
        part = form.part.data
        name = form.name.data
        Function.update_function_by_permission(part=part, name=name, permission=permission)
        return redirect(url_for("function.home"))
    tmp_function = Function.get_function_by_permission(permission)
    form.part.data = tmp_function.part
    form.name.data = tmp_function.name
    form.permission.data = tmp_function.permission
    return render_template("function/edit.html", form=form)


@function.route("/delete/<permission>")
@login_required
def delete(permission):
    Function.delete_function_by_permission(permission)
    return redirect(url_for("function.home"))




