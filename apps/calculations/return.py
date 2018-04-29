import datetime
import numpy as np


from apps.securities.services.security_data_services import get_price

def simple_return(security, period):
    pass

def log_return(security, period):
    now = datetime.today()
    past = datetime.timedelta(period)
    curr_price, past_price = get_price(security, now), get_price(security, past)
    return np.log(curr_price / past_price - 1)