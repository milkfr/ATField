import json
import requests
from requests.auth import HTTPBasicAuth

api_path = "http://127.0.0.1:8088/api/v1.0"
username = "aaa"
password = "123456"

# get token
r = requests.get(api_path+"/token", auth = HTTPBasicAuth(username, password))
token = json.loads(r.content.decode('utf-8'))["token"]
print(token)

# get old domain
r = requests.get(api_path+"/assets/domains?per_page=10000", auth = HTTPBasicAuth(token, ""))
# print(r.content)
old_domain_list = [item["name"] for item in json.loads(r.content.decode('utf-8'))["items"]]

# get new domain
with open("domain.txt") as f:
    domains = f.readlines()
domain_list = list(set([domain.strip() for domain in domains]))

# get add domain and get delete domain
delete_domain_list = list(set(old_domain_list).difference(set(domain_list)))
print(delete_domain_list)

add_domain_list = list(set(domain_list).difference(set(old_domain_list)))
print(add_domain_list)

# delete domain
r = requests.post(api_path+"/assets/domain/delete", auth = HTTPBasicAuth(token, ""), data=json.dumps(list(delete_domain_list)))
print(r.content)
if json.loads(r.content.decode('utf-8'))['status'] != "ok":
    print("delete domain err")
else:
    print("delete domain ok")

# add domain
data=json.dumps([{"name": domain, "description": ""} for domain in add_domain_list])
r = requests.post(api_path+"/assets/domain/add", auth = HTTPBasicAuth(token, ""), data=data)
print(r.content)
if json.loads(r.content.decode('utf-8'))['status'] != "ok":
    print("add domain err")
else:
    print("add domain ok")


# get old ip
r = requests.get(api_path+"/assets/hosts?per_page=10000", auth = HTTPBasicAuth(token, ""))
# print(r.content)
old_ip_list = [item["ip"] for item in json.loads(r.content.decode('utf-8'))["items"]]

# get new ip
with open("ip.txt") as f:
    ips = f.readlines()
ip_list = list(set([ip.strip() for ip in ips]))

# get add ip and get delete ip
delete_ip_list = list(set(old_ip_list).difference(set(ip_list)))
print(delete_ip_list)

add_ip_list = list(set(ip_list).difference(set(old_ip_list)))
print(add_ip_list)

# delete ip
r = requests.post(api_path+"/assets/host/delete", auth = HTTPBasicAuth(token, ""), data=json.dumps(list(delete_ip_list)))
print(r.content)
if json.loads(r.content.decode('utf-8'))['status'] != "ok":
    print("delete ip err")
else:
    print("delete ip ok")

# add ip
data=json.dumps([{"ip": ip, "name": "", "description": ""} for ip in add_ip_list])
r = requests.post(api_path+"/assets/host/add", auth = HTTPBasicAuth(token, ""), data=data)
print(r.content)
if json.loads(r.content.decode('utf-8'))['status'] != "ok":
    print("add ip err")
else:
    print("add ip ok")


