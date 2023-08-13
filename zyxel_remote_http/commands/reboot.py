from argparse import ArgumentParser
import sys
from time import sleep

import requests
from zyxel_remote_http.zyxel import Zyxel


class Reboot():
    def __init__(self):
        pass

    def add_options(self, subparser: ArgumentParser):
        subparser.add_argument('--wait', dest='wait', action='store_const', const=True)
        subparser.add_argument('--no-wait', dest='wait', action='store_const', const=False)

    def _wait(self, zyxel: Zyxel):
        print('waiting...')
        sleep(5)

        check_count = 0
        while check_count < 5:
            print(f'trying cmd 0, attempt {check_count+1}')
            check_count = check_count + 1
            try:
                response = zyxel.cmd(0)
                print('got', response.http_response.status_code)
                if response.http_response.status_code == 200:
                    print('ok')
                else:
                    print('fail: ' + str(response.http_response.status_code))
                break
            except requests.exceptions.ConnectionError:
                print('error, waiting again...')
                sleep(5)

    def do_command(self, zyxel: Zyxel, args):
        cmd = 5888
        wait = args.wait if args.wait is not None else True

        # Request the reboot form
        response = zyxel.cmd(cmd)

        # handle form_fields
        form = response.get_form()

        # submit the form
        (url, data) = form.get_form_url_and_data()
        response = zyxel.post(url, data)

        if response.http_response.status_code == 200:
            print('ok')
            if wait:
                self._wait(zyxel)
        else:
            print('fail: ' + str(response.http_response.status_code))
