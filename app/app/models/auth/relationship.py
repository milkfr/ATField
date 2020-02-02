from app.models import db, UUID
from sqlalchemy import Column, ForeignKey


RolePermission = db.Table(
    'auth_role_permission',
    Column('uk_role_uid', UUID, ForeignKey('auth_role.uid'), primary_key=True),
    Column('uk_permission_uid', UUID, ForeignKey('auth_permission.uid'), primary_key=True)
)


UserRole = db.Table(
    'auth_user_role',
    Column('uk_user_uid', UUID, ForeignKey("auth_user.uid"), primary_key=True),
    Column('uk_role_uid', UUID, ForeignKey("auth_role.uid"), primary_key=True)
)


