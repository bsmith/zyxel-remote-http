import sys
from urllib.parse import urljoin
from .response import Response
from .common import make_session, zyxelUrl
from .login import performLogin

class Zyxel():
    def __init__(self, host, fwversion):
        self.host = host
        self.fwversion = fwversion
        self.session = make_session()
        self.url_base = zyxelUrl(host)
        self.last_response = None
        self.verbose = False
    
    def set_verbose(self):
        self.verbose = True
    
    # returns the response passed in
    def _set_last_response(self, last_response):
        self.last_response = last_response
        return last_response

    def login(self, user, password):
        performLogin(self, self.url_base, user, password, self.fwversion)

    def request(self, method, url, data=None):
        url = urljoin(self.url_base, url)
        if self.verbose:
            redacted_data = dict(data if data else {})
            if 'password' in redacted_data:
                redacted_data['password'] = 'REDACTED'
            print('-> %s %s %s' % (method, url, redacted_data), file=sys.stderr)
        response = None
        if method == 'GET':
            response = self.session.get(url, params=data)
        elif method == 'POST':
            response = self.session.post(url, data)
        else:
            raise Exception("Can't do method %s" % method)
        if self.verbose:
            print('<- status %s' % response.status_code, file=sys.stderr)
        if response.ok:
            return self._set_last_response(Response(response))
        else:
            raise Exception("Failed to %s %s."
                            "Got response code %s: %s" % (method, url, response.status_code, response.text))
    
    def get(self, url, params=None):
        return self.request('GET', url, data=params)
    
    def post(self, url, data=None):
        return self.request('POST', url, data=data)
    
    def follow_redirect_if_present(self, response=None):
        if response == None:
            response = self.last_response
        redirect_url = response.search_for_location_replace()
        if self.verbose:
            print('-- follow_redirect_if_present:', redirect_url, file=sys.stderr)
        if redirect_url:
            return self.get(redirect_url)
        return response

    def cmd(self, cmd):
        return self.get(self.url_base, params={"cmd": cmd})
