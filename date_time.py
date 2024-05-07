import time
import datetime

def time_now():
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return time_now