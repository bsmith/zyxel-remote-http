#!/usr/bin/env python3

import argparse

from zyxel_remote_http import Zyxel
import zyxel_remote_http
from zyxel_remote_http.commands.cmd import Cmd
from zyxel_remote_http.commands.login import Login
from zyxel_remote_http.commands.ping import Ping

def main(args):
    # Connect to the zyxel and log in
    zyxel = Zyxel(host=args.host, fwversion=args.fwversion)
    if args.verbose:
        zyxel.set_verbose()
    zyxel.login(args.user, args.pwd)

    if hasattr(args.subcommand, 'do_command'):
        args.subcommand.do_command(zyxel, args)
    else:
        raise Exception('cannot execute command')

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
    parser.add_argument('--verbose', '-V', dest='verbose', action="store_true",
                        help='Trace requests make to the device on stderr.')
    
    subparsers = parser.add_subparsers(required=True)

    commands = {
        'cmd': Cmd(),
        'ping': Ping(),
        'login': Login()
    }

    for name, command in commands.items():
        subparser = subparsers.add_parser(name)
        subparser.set_defaults(subcommand=command)
        command.add_options(subparser)
    
    main(parser.parse_args())
