from flask import Blueprint

from app.api.restful.v1.asset import asset
from app.api.restful.v1.token import token


def create_blueprint_restful_v1():
    bp_restful_v1 = Blueprint('restful_v1', __name__)
    asset.register(bp_restful_v1)
    token.register(bp_restful_v1)
    return bp_restful_v1
