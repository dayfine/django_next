from apps.ycharts.api.base import BaseSecurityClient

class CompanyClient(BaseSecurityClient):
    SECURITY_TYPE_PATH = 'companies'
    VALID_SECURITY_FILTERS = ['benchmark_index', 'exchange', 'hq_region', 'incorporation_region',
                              'industry', 'is_lp', 'is_reit', 'is_shell', 'naics_industry',
                              'naics_sector', 'sector']