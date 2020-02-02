from app import create_app
from werkzeug.exceptions import HTTPException
from app.libs.errors import APIException
from app.libs.error_types import ServerException
from app.models import db
from app.models.auth import User, Role, Permission, RolePermission, UserRole
from app.models.asset import Host, Service, Domain, HTTP, CGI, Zone


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                User=User, Role=Role, Permission=Permission,
                RolePermission=RolePermission, UserRole=UserRole,
                Host=Host, Service=Service, Domain=Domain, HTTP=HTTP, CGI=CGI, Zone=Zone)


@app.cli.command()
def perup():
    with db.auto_commit():
        for item in Permission.query.all():
            db.session.delete(item)
    with db.auto_commit():
        for item in app.url_map.iter_rules():
            if item.endpoint != 'static':
                Permission.save(endpoint=item.endpoint)
        admin_role = Role.get_item_by_name(name='admin')
        admin_role.update(permissions=[permission for permission in Permission.list_items()])


@app.cli.command()
def deploy():
    db.drop_all()
    db.create_all()
    users = [
        {
            'name': 'admin@123.com',
            'password': '123456'
        },
    ]
    roles = [
        {'name': 'admin'},
    ]
    with db.auto_commit():
        for user in users:
            User.save(**user)
        for role in roles:
            Role.save(**role)
        for item in app.url_map.iter_rules():
            if item.endpoint != 'static':
                Permission.save(endpoint=item.endpoint)
    with db.auto_commit():
        admin_user = User.get_item_by_name(name='admin@123.com')
        admin_role = Role.get_item_by_name(name='admin')
        admin_role.update(permissions=[permission for permission in Permission.list_items()])
        admin_user.update(roles=[admin_role])
    with db.auto_commit():
        # Zone.save(name='test')
        zone = Zone.save(name='公网')
        Zone.save(name='私有云', parent_uid=zone.uid)
        Zone.save(name='公有云', parent_uid=zone.uid)
        Zone.save(name='内网')
    zone = Zone.query.filter(Zone.name == '公有云').first()
    import json
    with open('domain.txt') as f:
        domain_list = json.loads(f.read())
    with db.auto_commit():
        for domain in domain_list:
            Domain.save(zone_uid=zone.uid, **domain)
    with open('host.txt') as f:
        host_list = json.loads(f.read())
    with db.auto_commit():
        for host in host_list:
            Host.save(zone_uid=zone.uid, **host)
    with open('service.txt') as f:
        service_list = json.loads(f.read())
    with db.auto_commit():
        for service in service_list:
            Service.save(zone_uid=zone.uid, **service)


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 998
        return APIException(msg, code, error_code)
    else:
        if not app.config['DEBUG']:
            return ServerException()
        else:
            return e


if __name__ == '__main__':
    app.run(debug=True)
