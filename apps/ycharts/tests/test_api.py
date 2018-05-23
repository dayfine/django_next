import datetime
from unittest import mock, TestCase
from urllib.parse import urlencode
from urllib.error import HTTPError

import requests
import responses

from apps.ycharts.api.clients import CompanyClient


URL_RESPONSE_INDEX = {
    'https://ycharts.com/api/v3/companies/AAPL/points/price': {
        'response': {
            'AAPL': {
                'meta': {'status': 'ok'},
                'results': {
                    'price': {
                        'meta': {'status': 'ok'},
                        'data': ['2016-09-15', 115.39],
                    },
                },
            },
            'MSFT': {
                'meta': {'status': 'ok'},
                'results': {
                    'price': {
                        'meta': {'status': 'ok'},
                        'data': ['2016-09-15', 57.21],
                    },
                },
            },
        },
        'meta': {'url': 'http://ycharts.com/api/v3/companies/AAPL,MSFT/points/price',
                 'status': 'ok'},
    },
    'https://ycharts.com/api/v3/companies/AAPL/series/price?start_date=2016-09-10': {
        'response': {
            'AAPL': {
                'results': {
                    'price': {
                        'data': [['2016-09-12', 105.44], ['2016-09-13', 107.95],
                                 ['2016-09-14', 111.77], ['2016-09-15', 115.39]],
                        'meta': {'status': 'ok'},
                    },
                },
                'meta': {'status': 'ok'},
            },
        },
        'meta': {
            'url': 'http://ycharts.com/api/v3/companies/AAPL/series/price?start_date=2016-09-10',
            'status': 'ok'},
    },
    'https://ycharts.com/api/v3/companies/AAPL/info/name': {
        'response': {
            'AAPL': {
                'results': {
                    'name': {'data': 'Apple', 'meta': {'status': 'ok'}},
                },
                'meta': {'status': 'ok'},
            },
        },
        'meta': {'url': 'http://ycharts.com/api/v3/companies/AAPL/info/name', 'status': 'ok'},
    },
    'https://ycharts.com/api/v3/companies/TOOMANY/info/name': {
        'response': {},
        'meta': {
            'error_message': 'Too many identifiers. Ensure 100 or less.',
            'status': 'error',
            'error_code': 414,
            'url': 'http://ycharts.com/api/v3/companies/TOOMANY/info/name',
        },
    },
    'https://ycharts.com/api/v3/companies?page=1': {
        'response': [{'name': 'Apple', 'symbol': 'AAPL'},
                     {'name': 'Microsoft', 'symbol': 'MSFT'}],
        'meta': {
            'status': 'ok',
            'url': 'https://ycharts.com/api/v3/companies?page=1',
            'pagination_info': {
                'end_index': 2, 'num_items': 2, 'start_index': 1,
                'num_pages': 1, 'current_page_num': 1
            }
        }
    },
    'https://ycharts.com/api/v3/companies/AAPL/dividends?start_date=2015-01-01': {
        'meta': {
            'status': 'ok',
            'url': 'http://ycharts.com/api/v3/companies/AAPL/dividends?start_date=2015-01-01'
        },
        'response': {
            'AAPL': {
                'meta': {
                    'status': 'ok'
                },
                'results': [
                    {
                        'adjusted_dividend_amount': 0.47,
                        'currency_code': 'USD',
                        'declared_date': '2015-01-27',
                        'dividend_amount': 0.47,
                        'dividend_type': 'normal',
                        'ex_date': '2015-02-05',
                        'pay_date': '2015-02-12',
                        'record_date': '2015-02-09'
                    }
                ]
            }
        }
    },
    'https://ycharts.com/api/v3/companies/AAPL/splits?end_date=2014-01-01': {
        'meta': {
            'status': 'ok',
            'url': 'https://ycharts.com/api/v3/companies/AAPL/splits?end_date=2014-01-01'
        },
        'response': {
            'AAPL': {
                'meta': {
                    'status': 'ok'
                },
                'results': [
                    {
                        'day': '1987-06-16',
                        'is_stock_dividend': 'false',
                        'ratio': 2.0,
                        'status': 'executed'
                    }
                ]
            }
        }
    },
    'https://ycharts.com/api/v3/companies/GGP/spinoffs?end_date=2014-01-01': {
        'meta': {
            'status': 'ok',
            'url': 'https://ycharts.com/api/v3/companies/GGP/spinoffs?end_date=2014-01-01'
        },
        'response': {
            'GGP': {
                'meta': {
                    'status': 'ok'
                },
                'results': [
                    {
                        'child_company_exchange': 'null',
                        'child_company_symbol': 'NYU',
                        'day': '2010-11-10',
                        'ratio': 1.259958,
                        'status': 'executed'
                    }
                ]
            }
        }
    },
    'https://ycharts.com/api/v3/companies/AAPL/series/price?aggregate_function=max': {
        'response': {
            'AAPL': {
                'results': {
                    'price': {
                        'data': [['2016-09-12', 99999.00]],
                        'meta': {'status': 'ok'},
                    },
                },
                'meta': {'status': 'ok'},
            },
        },
        'meta': {
            'url': 'http://ycharts.com/api/v3/companies/AAPL/series/price?aggregate_function=max',
            'status': 'ok'},
    }
}

def mock_get_reponse(url, params, headers):
    full_url = '{0}?{1}'.format(url, urlencode(params)) if params else url
    return responses.Response(
        method='GET',
        url=full_url,
        headers=headers,
        json=URL_RESPONSE_INDEX[full_url],
        status=200,
    )

class ClientTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = CompanyClient('api_key')

    @responses.activate
    def test_successful_point_request(self):
        url = 'https://ycharts.com/api/v3/companies/AAPL/points/price'
        responses.add(responses.GET, url, json=URL_RESPONSE_INDEX[url], status=200)

        point_rsp = self.client.get_points(['AAPL'], ['price'])
        status = point_rsp['meta']['status']
        security_rsp_data = point_rsp['response']['AAPL']
        security_query_status = security_rsp_data['meta']['status']
        calc_rsp_data = security_rsp_data['results']['price']
        calc_query_status = calc_rsp_data['meta']['status']
        calc_query_data = calc_rsp_data['data']

        self.assertEqual(status, 'ok')
        self.assertEqual(security_query_status, 'ok')
        self.assertEqual(calc_query_status, 'ok')
        self.assertEqual(calc_query_data, ['2016-09-15', 115.39])

    @responses.activate
    def test_successful_series_request(self):
        url = 'https://ycharts.com/api/v3/companies/AAPL/series/price?start_date=2016-09-10'
        responses.add(responses.GET, url, json=URL_RESPONSE_INDEX[url], status=200)

        query_start_date = datetime.datetime(2016, 9, 10)
        series_rsp = self.client.get_series(['AAPL'], ['price'], query_start_date=query_start_date)
        status = series_rsp['meta']['status']
        security_rsp_data = series_rsp['response']['AAPL']
        security_query_status = security_rsp_data['meta']['status']
        calc_rsp_data = security_rsp_data['results']['price']
        calc_query_status = calc_rsp_data['meta']['status']
        calc_query_data = calc_rsp_data['data']

        self.assertEqual(status, 'ok')
        self.assertEqual(security_query_status, 'ok')
        self.assertEqual(calc_query_status, 'ok')
        expected_data = [['2016-09-12', 105.44], ['2016-09-13', 107.95],
                         ['2016-09-14', 111.77], ['2016-09-15', 115.39]]
        self.assertEqual(calc_query_data, expected_data)

    @responses.activate
    def test_successful_info_request(self):
        url = 'https://ycharts.com/api/v3/companies/AAPL/info/name'
        responses.add(responses.GET, url, json=URL_RESPONSE_INDEX[url], status=200)

        info_rsp = self.client.get_info_fields(['AAPL'], ['name'])
        status = info_rsp['meta']['status']
        security_rsp_data = info_rsp['response']['AAPL']
        security_query_status = security_rsp_data['meta']['status']
        info_response_data = security_rsp_data['results']['name']
        info_query_status = info_response_data['meta']['status']
        info_query_data = info_response_data['data']

        self.assertEqual(status, 'ok')
        self.assertEqual(security_query_status, 'ok')
        self.assertEqual(info_query_status, 'ok')
        self.assertEqual(info_query_data, 'Apple')

