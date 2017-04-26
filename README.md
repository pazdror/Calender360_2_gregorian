# Calender360_2_gregorian
convert Pandas Series\Dataframe with 360 day index to normal datetime index
____________________________________________________________________________


    Small function to convert Pandas object with 360day index to normal dates
    Developed for data extracted from NetCDF files with 360_day calendar type
    :param s: Pandas Series with 360-day date index
    :return: Pandas Series with normal dates, and values interpolate over each month
