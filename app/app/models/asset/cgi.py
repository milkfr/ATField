from app.models import BaseModel, UUID
from sqlalchemy import Column
from sqlalchemy.dialects.mysql.types import VARCHAR, SMALLINT, CHAR
from sqlalchemy.types import JSON


class CGI(BaseModel):

    __tablename__ = 'asset_cgi'
    http_uid = Column('idx_http_id', UUID, nullable=False, index=True)  # 多对一，HTTP
    url = Column(VARCHAR(256), nullable=False)  # url
    method = Column(CHAR(20), nullable=False)  # get, post...
    code = Column(SMALLINT(unsigned=True), nullable=False)  # status_code
    info = Column(JSON)  # request, response

    _fields = ['uid', 'http_uid', 'url', 'method', 'code', 'info']

    def _set_fields(self):
        self._fields = ['uid', 'http_uid', 'url', 'method', 'code', 'info']

    @classmethod
    def list_items_by_http_uid(cls, http_uid, status=1):
        return CGI.query.filter(CGI.status == status, CGI.http_uid == http_uid).all()

    @classmethod
    def get_item_by_uid(cls, uid, status=1):
        return CGI.query.filter(CGI.status == status, CGI.uid == uid).first()

    @classmethod
    def list_items_paginate_by_search(cls, page=1, per_page=10, uid=None, http_uid=None,
                                      status=1, url=None, method=None, code=None):
        query = CGI.query
        if uid:
            query = query.filter(CGI.uid == uid)
        if status in [0, 1]:
            query = query.filter(CGI.status == status)
        if http_uid:
            query = query.filter(CGI.http_uid == http_uid)
        if url:
            query = query.filter(CGI.url.ilike('%{}%'.format(url)))
        if method:
            query = query.filter(CGI.method == method)
        if code:
            query = query.filter(CGI.code == code)
        return query.paginate(
            page=page, per_page=per_page
        )
