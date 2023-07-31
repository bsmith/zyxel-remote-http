
from .login_v260 import performLogin as performLogin_v260
from .login_v270 import performLogin as performLogin_v270

def performLogin(session, url, username, password, version):
    if version == "260":
        performLogin_v260(session, url, username, password)
    elif version == "270":
        performLogin_v270(session, url, username, password)
    else:
        raise Exception("Not sure about version %s" % version)
