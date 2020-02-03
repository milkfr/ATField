from celery_worker import celery, es
from app.models.asset import Service
import time


class DailyHandleTask(celery.Task):

    name = 'master_daily_handle'

    def run(self):
        for service in Service.list_items_paginate_by_search(page=1, per_page=10000).items:
            es.index(index='master-host-{}'.format(time.strftime('%Y-%m-%d', time.localtime())), doc_type='doc', body={
                'ip': service.host_ip,
                'port': service.port,
                'name': service.name,
                'info': service.info
            })
