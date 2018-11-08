import os
import json
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db, es
from app.models.auth import User, Role, UserRole, Permission, RolePermission
from app.models.assets import Host, Domain, Service, HostDomain
from app.models.tasks import Task
from app.models.web import Application, Package, Plugin, ApplicationPlugin
from dotenv import load_dotenv


load_dotenv(dotenv_path=".flaskenv")

app = create_app(os.environ.get("FLASK_CONFIG", default="default"))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, es=es, Task=Task,
                User=User, Role=Role, UserRole=UserRole,
                Permission=Permission, RolePermission=RolePermission,
                Application=Application, Package=Package, Plugin=Plugin, ApplicationPlugin=ApplicationPlugin,
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
    permission_info_list = [
        {"name": "Web应用报文详情", "endpoint": "web.package_info"},
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
        {"name": "角色新增", "endpoint": "auth.role_new"},
        {"name": "权限列表查看", "endpoint": "auth.permission_list"},
        {"name": "主机资产查看", "endpoint": "assets.host_list"},
        {"name": "主机资产信息修改", "endpoint": "assets.host_update"},
        {"name": "服务资产查看", "endpoint": "assets.service_list"},
        {"name": "服务资产信息修改", "endpoint": "assets.service_update"},
        {"name": "域名资产查看", "endpoint": "assets.domain_list"},
        {"name": "域名资产信息修改", "endpoint": "assets.domain_update"},
        {"name": "任务列表查看", "endpoint": "tasks.task_list"},
        {"name": "任务详情查看", "endpoint": "tasks.info"},
        {"name": "Web应用列表查看", "endpoint": "web.application_list"},
        {"name": "Web应用信息修改", "endpoint": "web.application_update"},
        {"name": "Web应用报文列表查看", "endpoint": "web.package_list"},
        {"name": "Web应用报文备注修改", "endpoint": "web.package_update"},
        {"name": "Web应用报文详情", "endpoint": "web.package_info"},
        {"name": "Web扫描插件信息查看", "endpoint": "web.plugin_list"},
        {"name": "Web扫描插件信息修改", "endpoint": "web.plugin_update"},
        {"name": "新增Web应用", "endpoint": "web.application_new"},
        {"name": "新增Web扫描插件", "endpoint": "web.plugin_new"},
        {"name": "api_token", "endpoint": "api_v_1_0.get_token"},
        {"name": "api_host_list", "endpoint": "api_v_1_0.host_list"},
        {"name": "api_host_add", "endpoint": "api_v_1_0.host_add"},
        {"name": "api_host_delete", "endpoint": "api_v_1_0.host_delete"},
        {"name": "api_service_list", "endpoint": "api_v_1_0.service_list"},
        {"name": "api_domain_list", "endpoint": "api_v_1_0.domain_list"},
        {"name": "api_domain_add", "endpoint": "api_v_1_0.domain_add"},
        {"name": "api_domain_delete", "endpoint": "api_v_1_0.domain_delete"},
        {"name": "api_task_list", "endpoint": "api_v_1_0.task_list"},
        {"name": "api_application_list", "endpoint": "api_v_1_0.application_list"},
        {"name": "api_package_list", "endpoint": "api_v_1_0.package_list"},
        {"name": "api_plugin_list", "endpoint": "api_v_1_0.plugin_list"},
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
            host.update_asset_info(line["status"])
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
                domain.update_asset_info([j.address for j in i.items])
        except Exception as e:
            print(e)
