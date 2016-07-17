# -*- coding: utf-8 -*-

from flask import render_template
from . import main
from ..decorators.login_required import login_required


@main.route("/")
def home():
    return render_template("home.html", title="home")


@main.route("/admin")
@login_required
def admin():
    return render_template("home.html", title="admin")
