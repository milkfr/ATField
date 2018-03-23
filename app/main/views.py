from flask import abort, render_template, jsonify, url_for

from . import main
from ..models.auth import User


@main.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@main.route("/test/", defaults={'page': 1})
@main.route("/test/<int:page>/", methods=["GET", "POST"])
def test(page=1):
    theaders = ["id", "name", "password_hash"]
    pagination = User.query.order_by(User.id.desc()).paginate(
        page, per_page=5, error_out=False
    )
    return render_template('test.html', theaders=theaders, pagination=pagination, url='main.test')
