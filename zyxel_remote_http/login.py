
from .login_v260 import performLogin as performLogin_v260
from .login_v270 import performLogin as performLogin_v270

def performLogin(zyxel, url, username, password, version):
    if version == "260":
        performLogin_v260(zyxel, url, username, password)
    elif version == "270":
        performLogin_v270(zyxel, url, username, password)
    else:
        raise Exception("Not sure about version %s" % version)
