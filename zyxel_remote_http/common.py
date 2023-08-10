import requests

def make_session():
    session = requests.Session()
    # unfortunately, the ssl ciphers used by zyxel are very old and deprecated, thus plaintext HTTP
    session.verify = False
    return session

def zyxelUrl(host):
    return f"http://{host}/cgi-bin/dispatcher.cgi"
