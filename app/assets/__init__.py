from flask import Blueprint

probe = Blueprint("probe", __name__)

from . import views, forms
