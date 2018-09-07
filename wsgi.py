import os
import flask
from app import create_app, db, es
from app.models.auth import User, Role, UserRole, Permission, RolePermission

dotenv_path = os.path.join(os.path.dirname(__file__), ".flaskenv")
if os.path.exists(dotenv_path):
    flask.cli.load_dotenv(dotenv_path)

app = create_app(os.environ.get("FLASK_CONFIG", default="err"))


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, es=es,
                User=User, Role=Role, UserRole=UserRole,
                Permission=Permission, RolePermission=RolePermission)


@app.cli.command()
def fake():
    from app.fake import generate_fake_auth
    generate_fake_auth(url_map=app.url_map)


@app.cli.command()
def deploy():
    db.drop_all()
    db.create_all()
    # add user
    user_info_list = [
        {"name": "aaa", "department": "部门1", "password": "123456"},
        {"name": "bbb", "department": "部门1", "password": "123456"},
        {"name": "ccc", "department": "部门1", "password": "123456"},
    ]
    User.insert_items(user_info_list)

    # add role
    role_info_list = {
        {"name": "admin", "department": "特权"},
        {"name": "role1", "department": "部门1"},
        {"name": "role2", "department": "部门1"},
    }
    Role.insert_items(role_info_list)

    # add permission
    permission_info_list = [
        {"name": "用户列表查看", "endpoint": "auth.user_list"},
        {"name": "用户角色设定", "endpoint": "auth.user_update"},
        {"name": "角色列表查看", "endpoint": "auth.role_list"},
        {"name": "角色权限设定", "endpoint": "auth.role_update"},
        {"name": "权限列表查看", "endpoint": "auth.permission_list"},
    ]
    Permission.insert_items(permission_info_list)

    # add auth relationship
    admin_user = User.query.first()
    admin_role = Role.query.first()
    admin_user.update_role_by_id(delete_role_list=[], add_role_list=[admin_role.id])

    admin_role.update_permission_by_id(delete_permission_list=[],
                                       add_permission_list=[permission.id for permission in Permission.query.all()])
