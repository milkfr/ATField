import os
import json
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db, es
from app.models.auth import User, Role, UserRole, Permission, RolePermission
from app.models.probe import Host, Domain, Service, HostDomain
from app.models.tasks import Task
from dotenv import load_dotenv


load_dotenv(dotenv_path=".flaskenv")

app = create_app(os.environ.get("FLASK_CONFIG", default="default"))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, es=es, Task=Task,
                User=User, Role=Role, UserRole=UserRole,
                Permission=Permission, RolePermission=RolePermission,
                Host=Host, Domain=Domain, Service=Service, HostDomain=HostDomain)


@app.cli.command()
@click.option("--length", default=25,
              help="Number of functions to include in the profiler report.")
@click.option("--profile-dir", default=None,
              help="Directory where profiler data files are saved.")
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


@app.cli.command()
def fake():
    from app.fake import generate_fake_auth
    generate_fake_auth(url_map=app.url_map)


@app.cli.command()
def update():
    upgrade()
    permission_info_list = [
        {"name": "单次任务列表查看", "endpoint": "tasks.once_list"},
        {"name": "定时任务列表查看", "endpoint": "tasks.timed_list"},
        {"name": "新增任务", "endpoint": "tasks.new"},
        {"name": "任务详情查看", "endpoint": "tasks.info"},
    ]
    Permission.insert_items(permission_info_list)


@app.cli.command()
def deploy():
    upgrade()
    # db.drop_all()
    # db.create_all()
    # add user
    user_info_list = [
        {"name": "aaa", "department": "信息安全", "password": "123456"},
    ]
    User.insert_items(user_info_list)

    # add role
    role_info_list = [
        {"name": "admin", "department": "特权"},
        {"name": "role1", "department": "信息安全"},
        {"name": "role2", "department": "信息安全"},
    ]
    Role.insert_items(role_info_list)

    # add permission
    permission_info_list = [
        {"name": "用户列表查看", "endpoint": "auth.user_list"},
        {"name": "用户角色信息修改", "endpoint": "auth.user_update"},
        {"name": "角色列表查看", "endpoint": "auth.role_list"},
        {"name": "角色权限信息修改", "endpoint": "auth.role_update"},
        {"name": "权限列表查看", "endpoint": "auth.permission_list"},
        {"name": "主机资产查看", "endpoint": "probe.host_list"},
        {"name": "主机资产信息修改", "endpoint": "probe.host_update"},
        {"name": "服务资产设定", "endpoint": "probe.service_list"},
        {"name": "服务资产信息修改", "endpoint": "probe.service_update"},
        {"name": "域名资产查看", "endpoint": "probe.domain_list"},
        {"name": "域名资产信息修改", "endpoint": "probe.domain_update"},
        {"name": "下载文件", "endpoint": "main.download"},
    ]
    Permission.insert_items(permission_info_list)

    # add auth relationship
    admin_user = User.query.first()
    admin_role = Role.query.first()
    admin_user.update_role_by_id(delete_role_list=[], add_role_list=[admin_role.id])

    admin_role.update_permission_by_id(delete_permission_list=[],
                                       add_permission_list=[permission.id for permission in Permission.query.all()])

    # add host
    with open("ip.txt", "r") as f:
        host_info_list = []
        for line in f.readlines():
            line = json.loads(line)
            host_info_list.append({"ip": line["address"], "name": None, "description": None})
        Host.insert_items(host_info_list)

    # update host and add service
    with open("ip.txt", "r") as f:
        for line in f.readlines():
            line = json.loads(line)
            host = Host.query.filter(Host.ip == line["address"]).first()
            host.update_probe_info(line["status"])
            service_info_list = []
            for service in line["services"]:
                service_info_list.append(
                    {"ip": host.ip, "port": service["port"], "tunnel": service["tunnel"],
                     "protocol": service["protocol"], "state": service["state"],
                     "service": service["service"], "name": None, "description": None}
                )
            Service.insert_items(service_info_list)

    # add domain
    domain_info_list = []
    with open("domain.txt") as f:
        for line in f.readlines():
            line = line.strip()
            domain_info_list.append({"name": line, "description": None})
    Domain.insert_items(domain_info_list)

    # update domain
    for domain in Domain.query.all():
        import dns.resolver
        try:
            answer = dns.resolver.query(domain.name, 'A')
            for i in answer.response.answer:
                domain.update_probe_info([j.address for j in i.items])
        except Exception as e:
            print(e)
