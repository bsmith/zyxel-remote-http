import re
from bs4 import BeautifulSoup
import bs4
import requests
from .form import Form

class Response():
    http_response: requests.Response
    bs: BeautifulSoup
    form: bs4.Tag
    
    def __init__(self, http_response):
        self.http_response = http_response
        self.bs = None
        self.form = None

    def get_soup(self):
        if self.bs == None:
            self.bs = BeautifulSoup(self.http_response.text, 'html.parser')
        return self.bs

    def get_form(self):
        if self.form == None:
            self.form = Form(self.get_soup().form)
        return self.form
    
    def search_for_location_replace(self):
        redirect_match = re.search(r'window\.location\.replace\("([^"]+)"\)', self.http_response.text)
        if redirect_match:
            return redirect_match.group(1)
        return None