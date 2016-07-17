# -*- coding: utf-8 -*-

from flask import Blueprint

function = Blueprint("function", __name__)

from . import views, forms