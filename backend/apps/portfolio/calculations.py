from collections import OrderedDict
from datetime import date

from dateutil import relativedelta
import numpy as np
import pandas as pd


class DebtSecurity:
    def __init__(self, rate, maturity, payment_per_year, principal, start_date):
        self.rate = rate
        self.maturity = maturity
        self.payment_per_year = payment_per_year
        self.principal = principal
        self.start_date = date(**start_date)

    def calc_payment(self):
        payment = np.pmt(rate=self.rate/self.maturity,
                         nper=self.payment_per_year*self.maturity,
                         pv=self.principal)
        return round(payment,2)

    def calc_int_n_pcp_payment(self, period, additional_payment=0):
        ipmt = np.ipmt(rate=self.rate/self.maturity,
                       per=period,
                       nper=self.payment_per_year*self.maturity,
                       pv=self.principal)
        ppmt = np.ppmt(rate=self.rate/self.maturity,
                       per=period,
                       nper=self.payment_per_year*self.maturity,
                       pv=self.principal)
        return round(ipmt, 2), round(ppmt, 2)

    def calc_balance(self, period, additonal_payment=0):
        schedule = pd.DataFrame(self.amortize())
        schedule = schedule[[
            'Period', 'Month', 'Begin Balance', 'Payment', 'Interest',
            'Principal', 'Additional_Payment', 'End Balance'
        ]]
        schedule['Month'] = pd.to_datetime(schedule['Month'])


    def amortize(self, additional_payment=0):
        pmt = self.calc_payment()

        period, date = 1, self.start_date
        beg_bal = end_bal = self.principal

        while end_bal >  0:
            interest = round(((self.rate/self.maturity) * beg_bal), 2)
            pmt = min(pmt, beg_bal + interest)
            principal_reduction = pmt - interest
            principal_reduction += min(additional_payment, beg_bal - principal_reduction)

            end_bal = beg_bal - principal_reduction

            yield OrderedDict([
                ('Month', date),
                ('Period', period),
                ('Begin Balance', beg_bal),
                ('Payment', pmt),
                ('Principal', principal_reduction),
                ('Interest', interest),
                ('Additional_Payment', additional_payment),
                ('End Balance', end_bal),
            ])

            p += 1
            date += relativedelta(months=1)
            beg_bal = end_bal
