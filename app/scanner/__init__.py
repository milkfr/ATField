from celery_worker import celery
from scanner.master.host import HostHandleTask
from scanner.master.service import ServiceHandleTask
from scanner.master.domain import DomainHandleTask
from scanner.master.http import HTTPHandleTask
from scanner.master.cgi import CGIHandleTask
from scanner.master.special_nmap import SpecialNmapHandleTask
from scanner.master.special_http import SpecialHTTPHandleTask
from scanner.master.daily import DailyHandleTask


master_daily_handle = celery.tasks.register(DailyHandleTask())
master_host_handle = celery.tasks.register(HostHandleTask())
master_service_handle = celery.tasks.register(ServiceHandleTask())
master_domain_handle = celery.tasks.register(DomainHandleTask())
master_http_handle = celery.tasks.register(HTTPHandleTask())
master_cgi_handle = celery.tasks.register(CGIHandleTask())
master_special_nmap_handle = celery.tasks.register(SpecialNmapHandleTask())
master_special_http_handle = celery.tasks.register(SpecialHTTPHandleTask())
