import time
import datetime

def time_now():
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return time_now