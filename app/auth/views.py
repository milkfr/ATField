# -*- coding: utf-8 -*-


from flask import render_template, flash, redirect, url_for, session
from . import auth
from .forms import RegistrationForm, LoginForm
from ..models.users import User
from ..decorators.login_required import login_required


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user_by_email(form.email.data)
        if user is not None and user.verify_password(form.password.data):
            session["email"] = user.email
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
