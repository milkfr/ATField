from app.models import BaseModel, UUID
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql.types import CHAR
from app.models.asset import Domain, Host, Service, HTTP


class Zone(BaseModel):

    __tablename__ = 'asset_area'

    uid = Column(UUID, primary_key=True, nullable=False)
    name = Column(CHAR(36), nullable=False)  # 名称
    parent_uid = Column(UUID, ForeignKey("asset_area.uid"))  # 外键
    parent = relationship('Zone', backref='children', remote_side=[uid])

    _fields = ['uid', 'name', 'parent_uid']

    def _set_fields(self):
        self._fields = ['uid', 'name', 'parent_uid']

    @classmethod
    def recursion_items(cls, parent_uid=None, status=1):
        data = []
        for zone in Zone.query.filter(Zone.status == status, Zone.parent_uid == parent_uid):
            item = {
                'parent': zone
            }
            if zone.children:
                item['children'] = Zone.recursion_items(parent_uid=zone.uid, status=status)
            data.append(item)
        return data

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return Zone.query.filter(Zone.status == status, Zone.uid == uid).first()

    @classmethod
    def recursion_children_uid_list(cls, uid=None, status=1):
        data = []
        zone = Zone.get_item_by_uid(uid, status=status)
        if zone:
            data.append(zone.uid)
            for child in zone.children:
                data.extend(Zone.recursion_children_uid_list(uid=child.uid, status=status))
            return data

    def remove(self):
        hosts = Host.list_items_by_zone_uid(self.uid)
        for host in hosts:
            host.update(zone_uid=None)
        domains = Domain.list_items_by_zone_uid(self.uid)
        for domain in domains:
            domain.update(zone_uid=None)
        services = Service.list_items_by_zone_uid(self.uid)
        for service in services:
            service.update(zone_uid=None)
        https = HTTP.list_items_by_zone_uid(self.uid)
        for http in https:
            http.update(zone_uid=None)
        super().remove()
