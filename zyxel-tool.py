#!/usr/bin/env python3

import argparse
from zyxel_remote_http import Zyxel

def main(args):
    zyxel = Zyxel(host=args.host, fwversion=args.fwversion)
    zyxel.login(args.user, args.pwd)
    response = zyxel.cmd(args.cmd)
    if args.verbose:
        print(response)

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
