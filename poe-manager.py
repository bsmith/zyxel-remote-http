#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup

from zyxel_remote_http.common import make_session, zyxelUrl
from zyxel_remote_http import performLogin

def main(args):
    s = make_session()
    url = zyxelUrl(args.host)

    performLogin(s, url, args.user, args.pwd, args.fwversion)

    ret = s.get(url, params={"cmd": args.cmd})
    if ret.ok:
        soup = BeautifulSoup(ret.content, 'html.parser')
        print(soup)
    else:
        raise Exception("Failed call cmd %s."
                        "Got response: %s" % (args.cmd, ret.text))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Manage the PoE ports of a Zyxel GS1900-10HP switch.')
    parser.add_argument('--host', '-H', dest='host',
                        required=True, help='The hostname of the switch.')
    parser.add_argument('--user', '-U', dest='user',
                        required=True, help='An administrative user.')
    parser.add_argument('--password', '-P', dest='pwd',
                        required=True, help='Password of the admin user.')
    parser.add_argument('--fwversion', '-F', dest='fwversion',
                        required=True, help='Firmware version (260 or 270).')
    parser.add_argument('--cmd', '-c', dest='cmd',
                        required=True, help='cmd')
    parser.add_argument('--verbose', '-V', dest='verbose', action="store_true",
                        help='Return detailed information when querying the specified port state.')
    main(parser.parse_args())
