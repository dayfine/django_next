from abc import ABC
import datetime
from urllib.error import HTTPError

import requests

from apps.ycharts.api import exceptions


class BaseSecurityClient(ABC):

    API_BASE_URL = 'https://ycharts.com/api'
    API_VERSION = 'v3'
    MAX_LIST_LENGTH = 100
    SECURITY_TYPE_PATH = None
    VALID_SECURITY_FILTERS = None

    def __init__(self, api_key):
        self.header = {
            'X-YCHARTSAUTHORIZATION': api_key,
        }

    def get_securities(self):
        pass

    def get_points(self, security_symbols, calcs, query_date=None):
        security_symbols, calcs = self._str_or_list(security_symbols), self._str_or_list(calcs)

        url_path = self._build_url_path(security_symbols, 'points', calcs)
        params = {'date': self._format_query_date(query_date)} if query_date else None
        return self._get_data(url_path, params)

    def get_series(self, security_symbols, calcs, query_start_date=None, query_end_date=None,
        resample_frequency=None, resample_function=None, fill_method=None, aggregate_function=None):
        security_symbols = self._str_or_list(security_symbols)
        calcs = self._str_or_list(calcs)

        url_path = self._build_url_path(security_symbols, 'series', calcs)
        params = {}
        if query_start_date:
            params['start_date'] = self._format_query_date(query_start_date)
        if query_end_date:
            params['end_date'] = self._format_query_date(query_end_date)
        if resample_frequency:
            params['resample_frequency'] = resample_frequency
        if resample_function:
            params['resample_function'] = resample_function
        if fill_method:
            params['fill_method'] = fill_method
        if aggregate_function:
            params['aggregate_function'] = aggregate_function

        return self._get_data(url_path, params)

    def get_info_fields(self, security_symbols, info_fields):
        security_symbols = self._str_or_list(security_symbols)
        info_fields = self._str_or_list(info_fields)

        url_path = self._build_url_path(security_symbols, 'info', info_fields)
        return self._get_data(url_path, None)

    def _get_data(self, url_path, params=None):
        url = '{0}/{1}/{2}'.format(self.API_BASE_URL, self.API_VERSION, url_path)
        try:
            res = requests.get(url, params=params, headers=self.header)
        except HTTPError as http_error:
            if http_error.code == 404:
                raise exceptions.PyChartsRequestUrlNotFoundException()
            elif http_error.code == 401:
                raise exceptions.PyChartsRequestUnauthorizedException()
            elif http_error.code == 400:
                raise exceptions.PyChartsRequestException()
            else:
                raise

        return self._parse_response(res)

    def _parse_response(self, res):
        data = res.json()
        # raise any payload level errors
        if data['meta']['status'] == 'error':
            error_code = data['meta']['error_code']
            error_message = data['meta']['error_message']
            if error_code == 400:
                raise exceptions.PyChartsRequestException(error_message=error_message)
            elif error_code == 414:
                raise exceptions.PyChartsRequestTooLongException(error_message=error_message)

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

    def _format_query_date(self, query_date):
        if isinstance(query_date, datetime.datetime):
            return query_date.isoformat().split('T')[0]
        elif isinstance(query_date, int) and query_date < 0:
            return query_date
        else:
            error_message = 'Invalid Date paramter. Date should be a datetime object or a negative integer.'
            raise exceptions.PyChartsRequestException(error_message=error_message)

    def _str_or_list(self, arg):
        if not isinstance(arg, (list, tuple)) and arg is not None:
            arg = [arg]
        return arg