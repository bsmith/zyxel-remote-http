import requests

def make_session():
    s = requests.Session()
    # unfortunately, the ssl ciphers used by zyxel are very old and deprecated, thus plaintext HTTP
    s.verify = False
    return s

def zyxelUrl(host):
    return "http://{}/cgi-bin/dispatcher.cgi".format(host)