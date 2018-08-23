from flask import render_template, session, redirect, url_for, flash
from . import auth
from .forms import LoginForm
from ..models.auth import User


@auth.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter(User.name == login_form.username.data).first()
        if not user or not user.verify_password(login_form.password.data):
            return render_template("auth/login.html", form=login_form, flash=flash("用户名或密码错误"))
        for item in list(session.keys()):
            session.pop(item)
        session["id"] = user.id
        session["name"] = user.name
        return redirect(url_for("main.index"))
    return render_template("auth/login.html", form=login_form)


@auth.route("/logout", methods=["POST"])
def logout():
    for item in list(session.keys()):
        session.pop(item, None)
    return redirect(url_for("auth.login"))
