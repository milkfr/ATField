from flask import Blueprint

assets = Blueprint("assets", __name__)

from . import views, forms
