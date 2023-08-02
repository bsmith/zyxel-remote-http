#!/usr/bin/env python3

import argparse
import sys

from urllib.parse import urljoin

from zyxel_remote_http import Zyxel
import zyxel_remote_http

def main(args):
    # Connect to the zyxel and log in
    zyxel = Zyxel(host=args.host, fwversion=args.fwversion)
    if args.verbose:
        zyxel.set_verbose()
    zyxel.login(args.user, args.pwd)

    if args.subcommand == 'cmd':
        do_cmd(zyxel, args)
    elif args.subcommand == 'ping':
        do_ping(zyxel, args)

def do_cmd(zyxel, args):
    # Request the given cmd
    response = zyxel.cmd(args.cmd)
    if args.verbose:
        print(response, file=sys.stderr)
    
    # show the form
    if args.show_form:
        response.get_form().print_form()

    # handle form_fields
    for field in args.form_fields:
        if args.verbose:
            print("form-field:", field.split('='), file=sys.stderr)
        [field_name, field_value] = field.split('=')
        response.get_form().set_field(field_name, field_value)

    # submit the form
    if args.submit_form:
        (url, data) = response.get_form().get_form_url_and_data()
        response = zyxel.post(url, data)
        response = zyxel.follow_redirect_if_present(response)
        response_form = response.get_form()
        print(response_form.get_field('result'))

def do_ping(zyxel, args):
    cmd = 530
    # Request the given cmd
    response = zyxel.cmd(cmd)
    if args.verbose:
        print(response, file=sys.stderr)

    # handle form_fields
    form = response.get_form()
    if args.ping_ip != None:
        form.set_field('ip', args.ping_ip)
    if args.ping_count != None:
        form.set_field('count', args.ping_count)
    if args.ping_interval != None:
        form.set_field('interval', args.ping_interval)
    if args.ping_size != None:
        form.set_field('size', args.ping_size)

    # submit the form
    (url, data) = form.get_form_url_and_data()
    response = zyxel.post(url, data)
    response = zyxel.follow_redirect_if_present(response)
    response_form = response.get_form()
    if response_form:
        print(response_form.get_field('result'))
    else:
        print(response.http_response.text)

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

    parser_cmd = subparsers.add_parser('cmd')
    parser_cmd.set_defaults(subcommand='cmd')
    parser_cmd.add_argument('--cmd', '-c', dest='cmd',
                        required=True, help='cmd')
    parser_cmd.add_argument('--show-form', dest='show_form', action="store_true",
                        help='Extract and show any form on the returned page.')
    parser_cmd.add_argument('--form-field', dest='form_fields', action="append",
                        help='Fill in a form field, key=value.')
    parser_cmd.add_argument('--submit-form', dest='submit_form', action="store_true",
                        help='Submit the form on the returned page.')
    
    parser_ping = subparsers.add_parser('ping')
    parser_ping.set_defaults(subcommand='ping')
    parser_ping.add_argument('--ip', dest='ping_ip', required=True,
                             help='IP address to ping')
    parser_ping.add_argument('--count', dest='ping_count')
    parser_ping.add_argument('--interval', dest='ping_interval')
    parser_ping.add_argument('--size', dest='ping_size')
    
    main(parser.parse_args())
