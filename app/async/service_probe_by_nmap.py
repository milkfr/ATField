from app import celery
from datetime import datetime
from subprocess import call
from libnmap.parser import NmapParser
import os


@celery.task(bind=True)
def do_async_scan(self, targets, options):
    result = {
        "start_time": datetime.utcnow(),
        "end_time": datetime.utcnow(),
        "result": {
            "total": len(targets.split()),
            "failed": 0,
            "details": []
        }
    }
    count = 0
    self.update_state(state="PROGRESS", meta={'progress': count/len(targets.split())})

    for ip in targets.split():
        temp_file = "nmap.log"
        scan_cmd = "nmap {} -oX {} {}".format(options, temp_file, ip)
        call(scan_cmd, shell=True)

        item = {}

        try:
            parser_result = NmapParser.parse_fromfile(temp_file)
            item["start_time"] = parser_result.started
            item["end_time"] = parser_result.endtime
            item["elasped"] = parser_result.elapsed
            item["commandline"] = parser_result.commandline
            item["ip"] = ip
            item["error"] = ""
            item["services"] = []

            for host in parser_result.hosts:
                for service in host.services:
                    service_item = {
                        "port": service.port,
                        "tunnel": service.tunnel,
                        "protocol": service.protocol,
                        "state": service.state,
                        "service": service.service,
                        "banner": service.banner,
                    }
                    item["services"].append(service_item)
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception as e:
            item["error"] = e.__repr__()
            result["result"]["failed"] += 1

        result["result"]["details"].append(item)
        count += 1
        self.update_state(state="PROGRESS", meta={'progress': count/len(targets.split())})

    result["end_time"] = datetime.utcnow()
    return result
