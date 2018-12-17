from app import celery
from app.models.tasks import Task
from app.models.assets import Host, Service, Domain
import json


@celery.task
def save(result, id):
    task = Task.query.filter(Task.id == id).first()
    print(id)
    print(result)
    task.update_result(result=json.dumps(result["result"]))
    if task.func_type == "domain resolution":
        data = result["result"]["details"]
        for item in data:
            domain = Domain.query.filter(Domain.name == item["domain"]).first()
            domain.update_asset_info(item["ip"])
            domain.update_info(item["description"])
    elif task.func_type == "port monitor":
        data = result["result"]["details"]
        for item in data:
            for host_data in item["hosts"]:
                ip = host_data["address"]
                host = Host.query.filter(Host.ip == ip).first()
                host.update_asset_info(host_data["status"])
                port_list = [service["port"] for service in host_data["services"]]
                old_port_list = [service.port for service in host.services]
                delete_port_list = list(set(old_port_list).difference(set(port_list)))

                for port in delete_port_list:
                    service = Service.query.join(Host).filter(Host.ip == ip, Service.port == port).first()
                    service.delete_item()

                for service_data in host_data["services"]:
                    service = Service.query.join(Host).filter(Host.ip == ip, Service.port == service_data["port"]).first()
                    if service:
                        service.update_asset_info(service_data["tunnel"], service_data["protocol"],
                                                  service_data["state"], service_data["service"])
                    else:
                        Service.insert_items([{"ip": ip, "port": service_data["port"], "tunnel": service_data["tunnel"],
                                               "protocol": service_data["protocol"], "state": service_data["state"],
                                               "service": service_data["service"], "name": None, "description": None}])
