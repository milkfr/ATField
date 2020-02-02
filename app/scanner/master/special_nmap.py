from scanner.master.base import BaseHandleTask
from app.models.asset import Host
from celery_worker import celery
from app.models import db
from libnmap.parser import NmapParser


class SpecialNmapHandleTask(BaseHandleTask):

    name = 'master_special_nmap_handle'

    def get_target_list(self, target_option):
        db.session.close()
        target_list = [{
            'uid': None,
            'target': ' '.join([host.ip
                                for host in Host.list_items_paginate_by_search(**target_option).items])
        }]
        return target_list

    def get_plugin_list(self, plugin_option):
        plugin_list = [{'name': 'special_nmap', 'option': plugin_option.get('special_nmap')}]
        return plugin_list

    def get_success_callback(self):
        return callback_success

    def get_error_callback(self):
        return callback_error


@celery.task
def callback_success(results):
    parser_result = NmapParser.parse_fromstring(results[0].get('result'))
    for host in parser_result.hosts:
        services = []
        for service in host.services:
            if service.state == 'open':
                services.append({
                    'host_ip': host.address,
                    'port': service.port,
                    'protocol': service.protocol,
                    'tunnel': service.tunnel,
                    'name': service.service_dict.get('name'),
                    'cpe': ' '.join(service.service_dict.get('cpelist', [])),
                    'info': {
                        'status': service.state,
                        'banner': service.banner,
                        'fingerprint': service.servicefp[:500],
                        'product': service.service_dict.get('product'),
                        'version': service.service_dict.get('version'),
                        'extra': service.service_dict.get('extrainfo'),
                    }
                })
        try:
            os_match = host.os_match_probabilities()[0]
        except Exception as e:
            os_match = None
        with db.auto_commit():
            item = Host.get_item_by_ip(host.address)
            if item:
                item.update(
                    service_count=len(services),
                    cpe=' '.join(os_match.get_cpe()) if os_match else '',
                    info={
                        'status': host.status,
                        'hostname': ' '.join(host.hostnames),
                        'system': os_match.name if os_match else '',
                        'mac': host.mac,
                        'accuracy': os_match.accuracy if os_match else 0,
                        'fingerprint': host.os_fingerprint[:500]
                    },
                    services=services
                )


@celery.task
def callback_error(request, exc, traceback):
    print(request, exc, traceback)
