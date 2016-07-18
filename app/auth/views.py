# -*- coding: utf-8 -*-


from flask import render_template, flash, redirect, url_for, session
from . import auth
from .forms import RegistrationForm, LoginForm, UserRoleForm
from ..models.users import User
from ..decorators.login_required import login_required


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user_by_email(form.email.data)
        if user is not None and user.verify_password(form.password.data):
            session["email"] = user.email
            session["permission"] = user.get_permission_for_browser()
            return redirect(url_for("main.home"))
    return render_template("auth/login.html", title="login", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        User.add_new_user(form.email.data, form.password.data)
        flash("You can now login")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", title="register", form=form)


@auth.route("/logout")
@login_required
def logout():
    session.pop("email", None)
    return redirect(url_for("auth.login"))


@auth.route("/user", methods=["GET", "POST"])
@login_required
def user():
    form = UserRoleForm()
    tmp_user = User.get_user_by_email(session.get("email"))
    if form.validate_on_submit():
        tmp_user.bind_role_by_role_id(form.role.data)
        return redirect(url_for("main.home"))
    form.role.data = tmp_user.role_id
    return render_template("auth/user.html", form=form)
