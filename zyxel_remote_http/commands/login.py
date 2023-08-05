# Check for successful login by requesting the frameset with cmd=0

from zyxel_remote_http.zyxel import Zyxel


class Login():
    def add_options(self, subparser):
        # No options to set up
        pass

    def do_command(self, zyxel: Zyxel, args):
        response= zyxel.cmd(0)

        if response.http_response.status_code == 200:
            print('ok')
        else:
            print('fail')