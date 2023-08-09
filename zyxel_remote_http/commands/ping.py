from argparse import ArgumentParser
import sys
from zyxel_remote_http.zyxel import Zyxel


class Ping():
    def __init__(self):
        pass
    
    def add_options(self, subparser: ArgumentParser):
        subparser.add_argument('--ip', dest='ping_ip', required=True,
                                help='IP address to ping')
        subparser.add_argument('--count', dest='ping_count')
        subparser.add_argument('--interval', dest='ping_interval')
        subparser.add_argument('--size', dest='ping_size')

    def do_command(self, zyxel: Zyxel, args):
        cmd = 530
        # Request the given cmd
        response = zyxel.cmd(cmd)

        # handle form_fields
        form = response.get_form()
        if args.ping_ip is not None:
            form.set_field('ip', args.ping_ip)
        if args.ping_count is not None:
            form.set_field('count', args.ping_count)
        if args.ping_interval is not None:
            form.set_field('interval', args.ping_interval)
        if args.ping_size is not None:
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