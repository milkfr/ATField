#!/usr/bin/env python3
import dns.resolver
from datetime import datetime
import argparse
import logging
import time
import json


logging.basicConfig(level=logging.DEBUG,
                    format="[%(asctime)s %(filename)s(line:%(lineno)d)] %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="domain_resolution.log",
                    filemode='a')

start_time = time.time()


def do_scan(targets):
    result = {
        "start_time": datetime.utcnow(),
        "end_time": datetime.utcnow(),
        "result": {
            "total": len(targets.split()),
            "failed": 0,
            "details": []
        }
    }
    for domain in targets.split():
        try:
            answer = dns.resolver.query(domain, 'A')
            for i in answer.response.answer:
                result["result"]["details"].append({"domain": domain, "ip": [j.address for j in i.items], "error": ""})
        except Exception as e:
            result["result"]["details"].append({"domain": domain, "ip": None, "error": e.__repr__()})
            result["result"]["failed"] += 1
    result["end_time"] = datetime.utcnow()
    return result


def handler_result(result):
    with open("domain_resolution_{}.json".format(time.strftime("%Y%m%d%H%M", time.localtime(int(start_time)))), 'a') as f:
        f.write(json.dumps(result))


def command_parse():
    parser = argparse.ArgumentParser(description="A probe for finding ports and applications")

    parser.add_argument("-f", "--file", dest="target_file", nargs='?', required=True,
                        help="Specify targets from file")
    return parser.parse_args()


def main():
    args = command_parse()
    domain_list = []
    with open(args.target_file, "r") as f:
        for line in f.readlines():
            domain_list.append(line.strip())
    result = do_scan(' '.join(domain_list))
    handler_result(result)


if __name__ == "__main__":
    main()