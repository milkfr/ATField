import requests
import json
import time
import base64
from datetime import datetime
from .amqp import consuming

BASIC_URL = "https://localhost:8834"
WHITE_LIST = """
127.0.0.1
"""
HEADERS = {
    "X-API-Token": "CCAE0AC3-ACE5-4DD6-8B0C-AA56BD50D9FE",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36"
}

content = """
<html>
<title>HTML</title>
<style type="text/css">
</style>
</head>
<body>
<p>Nessus 例行扫描结果统计</p>
<table border="1">
  <tr>
    <th>target<th/>
    <th>critical</th>
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


def post(path, data):
    return requests.post(BASIC_URL + path, data=data, headers=HEADERS, verify=False)


def get(path):
    return requests.get(BASIC_URL + path, headers=HEADERS, verify=False)


def get_session():
    url = "/session"
    data = {"username": "kyo", "password": "123456"}
    response = post(url, json.dumps(data))
    data = json.loads(response.content.decode("utf-8"))
    return data["token"]


def get_template_uuid(name="advanced"):
    url = "/editor/policy/templates"
    response = get(url)
    data = json.loads(response.content.decode("utf-8"))
    for item in data["templates"]:
        if item["name"] == name:
            return item["uuid"]


def get_policy_id(name="diy_full"):
    url = "/policies"
    response = get(url)
    data = json.loads(response.content.decode("utf-8"))
    for item in data["policies"]:
        if item["name"] == name:
            return item["id"]


def get_folder_id(name="periodic task"):
    url = "/folders"
    response = get(url)
    data = json.loads(response.content.decode("utf-8"))
    for item in data["folders"]:
        if item["name"] == name:
            return item["id"]


def create_scan(name, template_uuid, policy_id, folder_id, targets):
    url = "/scans"
    targets = list(set(targets.split()).difference(set(WHITE_LIST.split())))
    data = {
        "uuid": template_uuid,  # required
        "settings": {
            "name": name,  # required
            "description": "periodic task",
            "policy_id": policy_id,
            "folder_id": folder_id,
            # "scanner_id": 0,
            "enabled": True,  # required
            # "launch": "",
            # "starttime": "20181224120200",
            # "rrules": "",
            # "timezone": "",
            "text_targets": ','.join(targets),  # "10.107.105.46",  # required
            # "file_targets": "",
            # "emails": "",
            # "acls": "",
        }
    }
    response = post(url, json.dumps(data))
    print(response.content)
    data = json.loads(response.content.decode("utf-8"))
    return data["scan"]["id"]


def start_scan(scan_id):
    url = "/scans/{}/launch".format(scan_id)
    # data = {"alt_targets": ["127.0.0.1", "10.107.105.46"]}
    data = {}
    response = post(url, json.dumps(data))
    data = json.loads(response.content.decode("utf-8"))
    print(data)


def get_report(scan_id, name):
    url = "/scans/{}".format(scan_id)
    response = get(url)
    response = json.loads(response.content.decode("utf-8"))
    count_critical = 0
    count_high = 0
    count_medium = 0
    count_low = 0
    count_info = 0
    count_list = []
    for host in response["hosts"]:
        ip = host["hostname"]
        critical = host["critical"]
        high = host["high"]
        medium = host["medium"]
        low = host["low"]
        info = host["info"]
        count_critical += int(critical)
        count_high += int(high)
        count_medium += int(medium)
        count_low += int(low)
        count_info += int(info)
        count_list.append(
            "<tr><td>{}<td/><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(ip, critical, high,
                                                                                                 medium, low, info))
    url = "/scans/{}/export".format(scan_id)
    data = {
        # "filter.0.filter": "severity",
        # "filter.0.quality": "neq",
        # "filter.0.value": "None",
        "chapters": "vuln_by_plugin",
        "format": "html"
    }
    response = post(url, data=json.dumps(data))
    data = json.loads(response.content.decode("utf-8"))
    token = data["token"]
    while True:
        time.sleep(3)
        response = get("/tokens/{}/status".format(token))
        if json.loads(response.content.decode("utf-8"))["status"] == "ready":
            break

    response = get("/tokens/{}/download".format(token))
    print("title: Nessus: {} | critical:{} high:{} medium:{} low:{} info:{}".format(name, count_critical, count_high,
                                                                                    count_medium, count_low, count_info))
    print("content: " + content.format("\n".join(count_list)))
    print("attachment_name: " + "{}.html".format(name))
    print("attachment_data: " + base64.b64encode(response.content).decode("utf-8"))


def get_scan_id_by_name(name):
    folder_id = get_folder_id("periodic task")
    response = get("/scans?folder_id={}".format(folder_id))
    response = json.loads(response.content.decode("utf-8"))
    for scan in response["scans"]:
        if scan["name"] == name:
            return scan["id"]


def callback(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    # """
    data = json.loads(body.decode("utf-8"))
    if data["options"] == "do scan":
        token = get_session()
        HEADERS["X-Cookie"] = "token={}".format(token)
        name = str(datetime.now()).split()[0]
        template_uuid = get_template_uuid("advanced")
        policy_id = get_policy_id("diy_full")
        folder_id = get_folder_id("periodic task")
        scan_id = create_scan(name, template_uuid, policy_id, folder_id, data["targets"])
        start_scan(scan_id)
    elif data["options"] == "get report":
        token = get_session()
        HEADERS["X-Cookie"] = "token={}".format(token)
        name = str(datetime.now()).split()[0]
        scan_id = get_scan_id_by_name(name)
        get_report(scan_id, name)
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    consuming("nessus", callback)
