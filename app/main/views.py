from flask import abort, render_template, jsonify, url_for, current_app, send_from_directory

from . import main
from ..models.auth import User
from ..email import send_email


@main.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@main.route("/test/", methods=["GET", "POST"])
def test():
    send_email(to="@qq.com", subject="Confirm test", template="tasks/test", user="123", token="345")
    return render_template("index.html")


@main.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(current_app.config['BASEDIR'], filename, as_attachment=True)
