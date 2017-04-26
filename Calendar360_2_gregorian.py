__author__ = 'Dror Paz'
__CreatedOn__ = '2017/04/26'

from datetime import date
import calendar
import numpy as np
import pandas as pd


def cal360_2_norm(s):
    '''
    Small function to convert Pandas object with 360day index to normal dates
    Developed for data extracted from NetCDF files with 360_day calendar type
    :param s: Pandas Series with 360-day date index
    :return: Pandas Series with normal dates, and values interpolate over each month
    '''
    print 'converting 360d to normal year'

    def get_day(d):
        if d.day == 1:
            # return first day of month
            return 1
        elif d.day == 30:
            # return last day of month
            return calendar.monthrange(d.year,d.month)[1]
        elif d.day in xrange(1,calendar.monthrange(d.year,d.month)[1]+1):
            # if day exist in month, return it
            return d.day
        else:
            # if day number does not exist in month, return last day of month (should only happen in February)
            return calendar.monthrange(d.year,d.month)[1]

    start_date = date(s.index[0].year,s.index[0].month,get_day(s.index[0]))
    end_YM=(s.index[-1].year,s.index[-1].month)
    end_date = date(end_YM[0],end_YM[1],get_day(s.index[-1]))

    # Create output time series
    out_s = pd.Series(index=pd.date_range(start_date,end_date, freq='D'))

    grouped = s.groupby(lambda x: (x.year,x.month))

    for g in grouped:
        '''
        for every month, interpolate the values over the real number of days.
        '''
        N = calendar.monthrange(*g[0])[1]
        x = np.linspace(1,N,30)
        y = g[1]
        new_x = np.arange(1,N+1)
        new_y = np.interp(new_x,x,y)
        new_index = [date(g[0][0],g[0][1],d) for d in new_x]
        out_s[new_index] = new_y
    return out_s
