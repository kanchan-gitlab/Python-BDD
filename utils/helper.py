"""
hosts helper functions
"""
from datetime import datetime


def get_current_time():
    """
    Construct a datetime from time.time()
    ex: datetime.datetime(2022, 7, 8, 18, 1, 22, 407328)
    :return: datetime object with date time details
    """
    return datetime.now()
