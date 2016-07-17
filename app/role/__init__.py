# -*- coding: utf-8 -*-


from flask import Blueprint

role = Blueprint("role", __name__)

from . import forms, views
