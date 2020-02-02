from app.models import BaseModel, UUID
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import VARCHAR
from sqlalchemy.types import JSON
from app.models.asset.cgi import CGI


class HTTP(BaseModel):

    __tablename__ = 'asset_http'
    website = Column(VARCHAR(256), nullable=False, unique=True)
    title = Column(VARCHAR(256))
    business = Column(VARCHAR(100))
    zone_uid = Column(UUID)  # zone_uid
    info = Column(JSON)  # status,banner,fingerprint,version,extra,product

    _fields = ['uid', 'website', 'title', 'business', 'zone_uid', 'info']

    def _set_fields(self):
        self._fields = ['uid', 'website', 'title', 'business', 'zone_uid', 'info']

    @property
    def cgi(self):
        return CGI.list_items_by_http_uid(http_uid=self.uid)

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return HTTP.query.filter(HTTP.status == status, HTTP.uid == uid).first()

    @classmethod
    def get_item_by_website(cls, website=None, status=1):
        return HTTP.query.filter(HTTP.status == status, HTTP.website == website).first()

    @classmethod
    def list_items_by_zone_uid(cls, zone_uid):
        return HTTP.query.filter(HTTP.zone_uid == zone_uid).all()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None, zone_list=None,
                                      website=None, title=None, business=None, status=1):
        query = HTTP.query
        if uid:
            query = query.filter(HTTP.uid == uid)
        if zone_list:
            query = query.filter(HTTP.zone_uid.in_(zone_list))
        if status in [0, 1]:
            query = query.filter(HTTP.status == status)
        if website:
            query = query.filter(HTTP.website.ilike('%{}%'.format(website)))
        if business:
            query = query.filter(HTTP.website.ilike('%{}%'.format(business)))
        if title:
            query = query.filter(HTTP.tunnel.ilike('%{}%'.format(title)))
        return query.paginate(
            page=page, per_page=per_page
        )
