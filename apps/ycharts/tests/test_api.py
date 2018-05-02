import datetime
import unittest
from unittest import mock, TestCase
import json
from pycharts.clients import CompanyClient


class MockHttpResponse(object):
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

    def __init__(self, request):
        self.request = request

    def read(self):
        return json.dumps(self.URL_RESPONSE_INDEX[self.request.get_full_url()])


def mock_urlopen(request):
    return MockHttpResponse(request)
