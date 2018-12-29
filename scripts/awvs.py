import json
import requests
from datetime import datetime
from .amqp import consuming


API_KEY = "1986ad8c0a5b3df4d7028d5f3c06e936c47704577335c4114b84a1efd3da23e17"
SCANNER_URL = "https://127.0.0.1:3443"
HEADERS = {"X-Auth": API_KEY, "content-type": "application/json"}
WHITE_LIST = """
127.0.0.1
"""
EMAIL = "abc@email.com"
PASSWORD = "abc@email.com"

content = """
<html>
<title>HTML</title>
<style type="text/css">
</style>
</head>
<body>
<p>AWVS 例行扫描结果统计</p>
<table border="1">
  <tr>
    <th>target<th/>
    <th>high</th>
    <th>medium</th>
    <th>low</th>
    <th>info</th>
  </tr>
  {}
</table>
</body>
</html>
"""


def get(api):
    return requests.get(SCANNER_URL+api, headers=HEADERS, verify=False)


def post(api, data):
    return requests.post(SCANNER_URL+api, data=json.dumps(data), headers=HEADERS, verify=False)


def delete(api):
    return requests.delete(SCANNER_URL+api, headers=HEADERS, verify=False)


def get_scan_id(target_id):
    response = get("/api/v1/scans")
    response = json.loads(response.content.decode("utf-8"))
    for result in response["scans"]:
        if result["target_id"] == target_id:
            return result["scan_id"]


def get_status(scan_id):
    response = get("/api/v1/scans/" + str(scan_id))
    response = json.loads(response.content.decode("utf-8"))
    return response["current_session"]["status"]


def get_reports():
    count_high = 0
    count_medium = 0
    count_low = 0
    count_info = 0
    count_list = []
    next_cursor = 0
    while True:
        response = get("/api/v1/targets?c={}".format(next_cursor))
        response = json.loads(response.content.decode("utf-8"))
        for target in response["targets"]:
            print(target)
            address = target["address"]
            high = target["severity_counts"]["high"] if target["severity_counts"] else 0 
            medium = target["severity_counts"]["medium"] if target["severity_counts"] else 0
            low = target["severity_counts"]["low"] if target["severity_counts"] else 0
            info = target["severity_counts"]["info"] if target["severity_counts"] else 0
            count_high += high
            count_medium += medium
            count_low += low
            count_info += info
            count_list.append("<tr><td>{}<td/><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(address, high, medium, low, info))
        next_cursor = response["pagination"]["next_cursor"]
        if not next_cursor:
            break
    print("title: AWVS: {} | high:{} medium:{} low:{} info:{}".format(str(datetime.now()).split()[0], count_high, count_medium, count_low, count_info))
    print("content: " + content.format('\n'.join(count_list)))


def clear_tasks():
    while True:
        response = get("/api/v1/targets")
        response = json.loads(response.content.decode("utf-8"))
        print(response)
        if response["targets"] == []:
            break
        for target in response["targets"]:
            delete("/api/v1/targets/" + str(target["target_id"]))


def add_task(target='', description=''):
    data = {"address": target, "description": description, "criticality": 10}
    response = post("/api/v1/targets", data=data)
    print(response.content)
    response = json.loads(response.content.decode("utf-8"))
    return response["target_id"]


def start_scan(target_id):
    data = {
        "target_id": target_id, 
        # "profile_id": "11111111-1111-1111-1111-111111111111"
        # "profile_id": "11111111-1111-1111-1111-111111111118"  # quick_profile_2
        # "profile_id": "11111111-1111-1111-1111-111111111117"  # Crawl Only
        # "profile_id": "11111111-1111-1111-1111-111111111116"  # Cross-site Scripting Vulnerabilities
        # "profile_id": "11111111-1111-1111-1111-111111111115"  # Weak Passwords
        # "profile_id": "11111111-1111-1111-1111-111111111114"  # quick_profile_1
        # "profile_id": "11111111-1111-1111-1111-111111111113"  # SQL Injection Vulnerabilities
        # "profile_id": "11111111-1111-1111-1111-111111111112"  # High Risk Vulnerabilities
        "profile_id": "11111111-1111-1111-1111-111111111111",  # Full Scan
        "schedule": {
            "disable": False, 
            "start_date": None, 
            "time_sensitive": False
        }
    }
    response = post("/api/v1/scans", data=data)
    response = json.loads(response.content.decode("utf-8"))
    return response["target_id"]


def callback(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    data = json.loads(body.decode("utf-8"))
    if data["options"] == "do scan":
        clear_tasks()
        for target in data["targets"].split():
            print(target.split(":")[1][2:])
            target_id = None
            if target.split(":")[1][2:] not in WHITE_LIST:
                target_id = add_task(target=target, description=target)
            start_scan(target_id)
    elif data["options"] == "get report":
        get_reports()
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    consuming("awvs", callback)
