from app.models import BaseModel, UUID
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import VARCHAR, CHAR, SMALLINT
from app.models.asset.service import Service
from sqlalchemy.types import JSON


class Host(BaseModel):

    __tablename__ = 'asset_host'

    ip = Column('uk_ip', CHAR(19), nullable=False, unique=True)  # IP
    origin = Column(VARCHAR(64))  # 数据来源
    service_count = Column(SMALLINT(unsigned=True), nullable=False, default=0)  # 服务个数
    cpe = Column(VARCHAR(256))  # cpe
    info = Column(JSON)  # status,hostname,accuracy,mac,fingerprint,system
    zone_uid = Column(UUID)  # zone_uid

    _fields = ['uid', 'ip', 'origin', 'cpe', 'service_count', 'info', 'zone_uid']

    def _set_fields(self):
        self._fields = ['uid', 'ip', 'origin', 'cpe', 'service_count', 'info', 'zone_uid']

    def remove(self):
        for service in Service.list_items_by_host_uid(host_uid=self.uid):
            service.remove()
        self.service_count = 0
        super().remove()

    @property
    def services(self):
        return Service.list_items_by_host_uid(host_uid=self.uid)

    @services.setter
    def services(self, new_services):
        self.service_count = len(new_services)
        old_services = Service.list_items_by_host_uid(host_uid=self.uid)
        new_service_port = [service['port'] for service in new_services]
        old_service_port = [service.port for service in old_services]
        remove_service_port = list(set(old_service_port).difference(set(new_service_port)))
        for service in old_services:
            if service.port in remove_service_port:
                service.remove()
            else:
                for new_service in new_services:
                    if new_service['port'] == service.port:
                        service.update(**new_service)
        save_service_port = list(set(new_service_port).difference(set(old_service_port)))
        for port in save_service_port:
            for service in new_services:
                if service['port'] == port:
                    Service.save(host_uid=self.uid, zone_uid=self.zone_uid, **service)

    @classmethod
    def get_item_by_ip(cls, ip=None, status=1):
        query = Host.query.filter(Host.status == status, Host.ip == ip)
        return query.first()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return Host.query.filter(Host.status == status, Host.uid == uid).first()

    @classmethod
    def list_items(cls, status=1):
        return Host.query.filter(Host.status == status).all()

    @classmethod
    def list_items_by_zone_uid(cls, zone_uid):
        return Host.query.filter(Host.zone_uid == zone_uid).all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None, zone_list=None,
                                      ip=None, status=1, cpe=None, origin=None):
        query = Host.query
        if uid:
            query = query.filter(Host.uid == uid)
        if zone_list:
            query = query.filter(Host.zone_uid.in_(zone_list))
        if status in [0, 1]:
            query = query.filter(Host.status == status)
        if ip:
            query = query.filter(Host.ip.ilike('%{}%'.format(ip)))
        if cpe:
            query = query.filter(Host.cpe.ilike('%{}%'.format(cpe)))
        if origin:
            query = query.filter(Host.origin == origin)
        return query.paginate(
            page=page, per_page=per_page
        )
