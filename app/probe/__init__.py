from flask import Blueprint

asset = Blueprint("asset", __name__)

from . import views, forms
