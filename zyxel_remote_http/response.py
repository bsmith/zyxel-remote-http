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
        self._bs = None
        self._form = None

    def get_soup(self):
        if self._bs == None:
            self._bs = BeautifulSoup(self.http_response.text, 'html.parser')
        return self._bs

    def get_form(self):
        if self._form == None:
            form_tag = self.get_soup().form
            if form_tag:
                self._form = Form(form_tag)
            else:
                return None
        return self._form
    
    def search_for_location_replace(self):
        replace_match = re.search(r'window\.location\.replace\("([^"]+)"\)', self.http_response.text)
        if replace_match:
            return replace_match.group(1)
        href_match = re.search(r'window\.location\.href = "([^"]+)";', self.http_response.text)
        if href_match:
            return href_match.group(1)
        return None

    def extract_table(self):
        bs = self.get_soup()
        dataset = []
        for row_tag in bs.find_all('tr'):
            row_data = []
            for cell_tag in row_tag.find_all('td', recursive=False):
                value = ' '.join(cell_tag.stripped_strings)
                if value.strip() != '':
                    row_data.append(value)
            if len(row_data):
                dataset.append(row_data)
        return dataset