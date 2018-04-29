import abc
import requests

API_BASE_URL = 'https://ycharts.com/api'
API_VERSION = 3

class BaseSecurityClient(abc):
    def __init__(self, api_key):
        self.header = {
            'X-YCHARTSAUTHORIZATION': api_key,
        }


    def get_securities(self):
        pass


    def get_results(self):
        r = requests.get(url='', params={}, )