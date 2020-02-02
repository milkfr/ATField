from app.api.manager.auth import create_blueprint_auth
from app.api.manager.asset import create_blueprint_asset


def create_blueprint_manager():
    return [create_blueprint_auth(), create_blueprint_asset()]
