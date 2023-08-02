from .response import Response
from .common import make_session, zyxelUrl
from .login import performLogin

class Zyxel():
    def __init__(self, host, fwversion):
        self.host = host
        self.fwversion = fwversion
        self.session = make_session()
        self.url_base = zyxelUrl(host)

    def login(self, user, password):
        performLogin(self.session, self.url_base, user, password, self.fwversion)

    def cmd(self, cmd):
        ret = self.session.get(self.url_base, params={"cmd": cmd})
        if ret.ok:
            # print(ret.text)
            return Response(ret)
        else:
            raise Exception("Failed to call cmd %s."
                            "Got response: %s" % (cmd, ret.text))
