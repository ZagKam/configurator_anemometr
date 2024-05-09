import cProfile

from pstats import Stats, SortKey

def profileit(func):
    def wrapper(*args, **kwargs):
        print(func)
        with cProfile.Profile() as pr:
            result = func(*args, **kwargs)
        
        Stats(pr).sort_stats(SortKey.TIME).print_stats(10) # sort by total execution time and limit output to 10 lines
        return result

    return wrapper

from random import random
from threading import Thread
from time import sleep, time

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview


curparam_coldata = [
    "Время",
    "Скорость",
    "Направление",
    "М12",
    "М21",
    "М34",
    "М43",
    "Т1",
    "Т2",
    "Т3",
    "Т4"
]
class CurParamTable(Tableview):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, 
            coldata=curparam_coldata,
            rowdata=[],
            paginated=True,
            delimiter=",",
            **kwargs)
    
    
    def sort_by_date(self):
        self.sort_column_data(cid=0, sort=1)

    @profileit
    def sort_column_data(self, event=None, cid=None, sort=None):
        return super().sort_column_data(event, cid, sort)
    
    @profileit
    def load_table_data(self, clear_filters=False):
        return super().load_table_data(clear_filters)
    

def add_row():
    for i in range(100):
        values = [int(time())]
        values.extend([round(random() * 255) for _ in range(len(curparam_coldata)-1)])

        dt.insert_row("end",
            values
        )
        dt.sort_by_date()
      



root = ttk.Window(themename="united")
dt = CurParamTable(root)

dt.pack()
Thread(target=add_row, daemon=True).start()
root.mainloop()