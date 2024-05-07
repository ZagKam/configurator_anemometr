from datetime import datetime
from date_time import time_now
#from pathlib
import os


def add_line(c1: float, c2: float):
    """Add new line to log file

    :param datetime: _description_
    :type datetime: datetime
    :param c1: _description_
    :type c1: float
    :param c2: _description_
    :type c2: float
    """
    device_name = 'Logger'
    
    time = time_now()
    write_path = device_name + '.csv'
    mode = 'a' if os.path.exists(write_path) else 'w'
    with open(write_path, mode) as file:
        try:
            if mode == 'w':  
                file.write('SEP=,\nDate,  c1, c2, \n')
            file.write(f"{time},{c1},{c2}")                            
        except Exception as e:
            print(e)