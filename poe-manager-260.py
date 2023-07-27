#!/usr/bin/env python3

import math
import argparse
import requests
from random import random
from time import sleep, time
from bs4 import BeautifulSoup

from lib.login_v260 import encode
from lib.common import make_session, zyxelUrl

def main(args):
    s = make_session()
    url = zyxelUrl(args.host)

    login_data = {
        "login": 1,
        "username": args.user,
        "password": encode(args.pwd),
        "dummy": current_time()
    }
    login_check_data = {
        "login_chk": 1,
        "dummy": current_time()
    }

    print("Logging in...")
    s.get(url, params=login_data)
    # implicitly wait for login to occur
    sleep(1)
    ret2 = s.get(url, params=login_check_data)
    # 'OK' if logged in
    # 'AUTHING' if not logged in
    if 'OK' not in ret2.text:
        raise Exception("Login failed: %s" % ret2.text)

    print("Login successful, parsing cookie.")
    cookie = parse_cookie(s.get(url, params={"cmd": 2}))
    print("Got COOKIE: %s" % cookie)
    s.cookies.set("XSSID", cookie)

    print(s.cookies)
    print(s.cookies.get("HTTP_XSSID"))

    ret = s.get(url, params={"cmd": 799})
    if ret.ok:
        soup = BeautifulSoup(ret.content, 'html.parser')
        # print("Got soup %s" % soup)
    else:
        raise Exception("Failed to fetch the state of PoE port %s."
                        "Got response: %s" % (args.port, ret.text))
    # if args.state is None:
    #     table = soup.select("table")[2]
    #     data = []
    #     # https://stackoverflow.com/a/23377804
    #     for row in table.find_all('tr'):
    #         cols = row.find_all('td')
    #         cols = [ele.text.strip() for ele in cols]
    #         data.append([ele for ele in cols if ele])

    #     ret = []
    #     for entry in data[3:]:
    #         if entry:
    #             entr = {}
    #             for i, item in enumerate(entry[:-1]):
    #                 entr[data[0][i]] = item
    #             ret.append(entr)
    #     if args.port:
    #         if args.verbose:
    #             output = ret[args.port - 1]
    #         else:
    #             output = ret[args.port - 1].get("State")
    #     else:
    #         output = ret
    #     print(output)
    # else:
    #     xssid_content = soup.find('input', {'id': 'XSSID'}).get('value')
    #     print("Executing command: Turn %s PoE Port %s." %
    #           ('on' if args.state else 'off', args.port))
    #     command_data = {
    #         "XSSID": xssid_content,
    #         "portlist": args.port,
    #         "state": args.state,
    #         "portPriority": 2,
    #         "portPowerMode": 3,
    #         "portRangeDetection": 0,
    #         "portLimitMode": 0,
    #         "poeTimeRange": 20,
    #         "cmd": 775,
    #         "sysSubmit": "Apply"
    #     }
    #     ret = s.post(url, data=command_data)
    #     if 'window.location.replace' in ret.text:
    #         print("Command executed successfully!")
    #     else:
    #         raise Exception("Failed to execute command: %s" % ret.text)


def current_time():
    return int(time() * 1000.0)


def parse_cookie(cmd_1: requests.Response):
    print(cmd_1.text)
    for line in cmd_1.text.split("\n"):
        if 'XSSID' in line:
            return line.replace('setCookie("XSSID", "', '').replace('");', '').strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Manage the PoE ports of a Zyxel GS1900-10HP switch.')
    parser.add_argument('--host', '-H', dest='host',
                        required=True, help='The hostname of the switch.')
    parser.add_argument('--user', '-U', dest='user',
                        required=True, help='An administrative user.')
    parser.add_argument('--password', '-P', dest='pwd',
                        required=True, help='Password of the admin user.')
    parser.add_argument('--port', '-p', dest='port', type=int, required=True,
                        help='The port number. When querying information, 0 means all ports.')
    parser.add_argument('--state', '-s', dest='state', type=int,
                        choices=[0, 1],
                        help='Turn the port on (1) or off (0). To query the state, rather than set it, omit this parameter.')
    parser.add_argument('--verbose', '-V', dest='verbose', action="store_true",
                        help='Return detailed information when querying the specified port state.')
    main(parser.parse_args())
