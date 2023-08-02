#!/usr/bin/env python3

import argparse
import re
import sys

from urllib.parse import urljoin

from zyxel_remote_http import Zyxel
import zyxel_remote_http

def main(args):
    # Connect to the zyxel and log in
    zyxel = Zyxel(host=args.host, fwversion=args.fwversion)
    zyxel.login(args.user, args.pwd)

    # Request the given cmd
    response = zyxel.cmd(args.cmd)
    if args.verbose:
        print(response)
    
    # show the form
    if args.show_form:
        print("show form")
        response.get_form().print_form()

    # handle form_fields
    for field in args.form_fields:
        if args.verbose:
            print("form-field:", field.split('='))
        [field_name, field_value] = field.split('=')
        response.get_form().set_field(field_name, field_value)

    # submit the form
    if args.submit_form:
        (url, data) = response.get_form().get_form_url_and_data()
        url = urljoin(zyxel.url_base, url)
        if args.verbose:
            print('POST', url)
            print(data)
        response = zyxel.session.post(url, data)
        print(response)
        redirect_match = re.search(r'window\.location\.replace\("([^"]+)"\)', response.text)
        if redirect_match:
            print(redirect_match.group(1))
            url = urljoin(zyxel.url_base, redirect_match.group(1))
            response = zyxel.session.get(url)
            print(response)
            response_form = zyxel_remote_http.Response(response).get_form()
            print(response_form.get_field('result'))
        

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
    parser.add_argument('--show-form', dest='show_form', action="store_true",
                        help='Extract and show any form on the returned page.')
    parser.add_argument('--form-field', dest='form_fields', action="append",
                        help='Fill in a form field, key=value.')
    parser.add_argument('--submit-form', dest='submit_form', action="store_true",
                        help='Submit the form on the returned page.')
    parser.add_argument('--verbose', '-V', dest='verbose', action="store_true",
                        help='Return detailed information when querying the specified port state.')
    main(parser.parse_args())
