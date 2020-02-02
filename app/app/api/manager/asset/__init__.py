from flask import Blueprint


from app.api.manager.asset.host import host
from app.api.manager.asset.domain import domain
from app.api.manager.asset.service import service
from app.api.manager.asset.http import http
from app.api.manager.asset.cgi import cgi
from app.api.manager.asset.zone import zone


def create_blueprint_asset():
    bp_asset = Blueprint('manager_asset', __name__)
    host.register(bp_asset)
    domain.register(bp_asset)
    service.register(bp_asset)
    http.register(bp_asset)
    cgi.register(bp_asset)
    zone.register(bp_asset)
    return bp_asset
