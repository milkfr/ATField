from flask import abort, render_template, jsonify

from . import main
from ..models.auth import User


@main.route('/', methods=["GET"])
def index():
    user = User.query.all()
    return render_template("test.html")


@main.route("/test", methods=["GET", "POST"])
def test():
    table = dict()
    table["header"] = ["编号", "姓名", "密码"]
    table["data"] = []
    pagination = User.query.order_by(User.id.desc()).paginate(
        10, per_page=3, error_out=False
    )
    for u in pagination.items:
        table["data"].append({"id": u.id, "name": u.name, "password": u.password_hash})
    table['has_prev'] = pagination.has_prev
    table['has_next'] = pagination.has_next
    table['pages'] = list(pagination.iter_pages())
    table['page'] = pagination.page
    data = dict()
    data["table"] = table
    return jsonify(data)
