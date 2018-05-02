import abc
import datetime
from urllib.error import HTTPError

import requests


class BaseSecurityClient(abc):

    API_BASE_URL = 'https://ycharts.com/api'
    API_VERSION = 3
    MAX_LIST_LENGTH = 100

    def __init__(self, api_key):
        self.header = {
            'X-YCHARTSAUTHORIZATION': api_key,
        }

    def get_securities(self):
        pass

    def get_points(self, security_symbols, calcs, query_date=None):
        url_path = self._build_url_path(security_symbols, 'points', calcs)
        if query_date:
            params = {'date': self._format_query_date_for_url(query_date)}
        else:
            params = None

    def get_series(self):
        pass

    def get_info_fields(self):
        pass

    def _get_data(self, url_path, params=None):
        url = '{0}/{1}/{2}'.format(self.BASE_URL, self.API_VERSION, url_path)
        res = requests.get(url, params=params, headers=self.header)
        return self._parse_response(res)

    def _parse_response(self, res):
        data = res.json()
        # raise any payload level errors
        if data['meta']['status'] == 'error':
            error_code = data['meta']['error_code']
            error_message = data['meta']['error_message']
            raise HTTPError(code=error_code, msg=error_message)
        return data

    def _build_url_path(self, security_symbols, query_type_path, query_keys=None):
        url_path = self.SECURITY_TYPE_PATH

        if security_symbols and query_type_path:
            security_symbol_params = ','.join(security_symbols[:self.MAX_LIST_LENGTH])
            url_path = '{0}/{1}/{2}'.format(url_path, security_symbol_params, query_type_path)

        if query_keys:
            query_key_params = ','.join(query_keys[:self.MAX_LIST_LENGTH])
            url_path = '{0}/{1}'.format(url_path, query_key_params)

        return url_path

    def _format_query_date_for_url(self, query_date):
        if isinstance(query_date, datetime.datetime):
            return query_date.isoformat().split('T')[0]
        elif isinstance(query_date, int) and query_date < 0:
            return query_date
        else:
            raise TypeError('Invalid Date paramter. Date should be a datetime '
                            'object or a negative integer.')