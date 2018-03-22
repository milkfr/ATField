from flask import abort, render_template, session, redirect, url_for
from . import auth
from .forms import LoginForm


@auth.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session["username"] = login_form.username.data
        return redirect(url_for("main.index"))
    return render_template("auth/login.html", form=login_form)


@auth.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("auth.login"))
