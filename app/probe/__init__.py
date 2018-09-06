from flask import Blueprint

probe = Blueprint("asset", __name__)

from . import views, forms
