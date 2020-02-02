from app.models import BaseModel, UUID
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import VARCHAR, TINYINT
from sqlalchemy.types import JSON


class Domain(BaseModel):

    __tablename__ = 'asset_domain'

    name = Column('uk_name', VARCHAR(64), nullable=False, unique=True)  # 域名
    type = Column(TINYINT(unsigned=True))  # DNS解析类型
    origin = Column(VARCHAR(64))  # 数据来源
    info = Column(JSON)
    zone_uid = Column(UUID)  # zone_uid

    _fields = ['uid', 'name', 'type', 'origin', 'info', 'zone_uid']

    def _set_fields(self):
        self._fields = ['uid', 'name', 'type', 'origin', 'info', 'zone_uid']

    @classmethod
    def list_items_by_zone_uid(cls, zone_uid, status=1):
        return Domain.query.filter(Domain.status == status, Domain.zone_uid == zone_uid).all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None, zone_list=None,
                                      name=None, type=None, origin=None, status=1):
        query = Domain.query
        if uid:
            query = query.filter(Domain.uid == uid)
        if zone_list:
            query = query.filter(Domain.zone_uid.in_(zone_list))
        if status in [0, 1]:
            query = query.filter(Domain.status == status)
        if name:
            query = query.filter(Domain.name.ilike('%{}%'.format(name)))
        if type:
            query = query.filter(Domain.type == type)
        if origin:
            query = query.filter(Domain.origin.ilike('%{}%'.format(origin)))
        return query.paginate(
            page=page, per_page=per_page
        )

    @classmethod
    def get_item_by_name(cls, name, status=1):
        return Domain.query.filter(Domain.status == status, Domain.name == name).first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return Domain.query.filter(Domain.status == status, Domain.uid == uid).first()
