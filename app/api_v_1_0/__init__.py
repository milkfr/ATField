from flask import Blueprint

api_v_1_0 = Blueprint("api_v_1_0", __name__)

from . import views, auth
