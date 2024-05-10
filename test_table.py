from threading import Thread
from random import randint
import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

from ttkbootstrap.localization import MessageCatalog
from ttkbootstrap.constants import *
from time import sleep, time


class CalibrationLoader(ttk.Meter):
    ...

class CurParamTable(Tableview):

    def __init__(self, *args, **kwargs):
        
        self.autoscroll = tk.BooleanVar(root)
        self.autoscroll.set(True)
        super().__init__(
            *args, 
            rowdata=[],
            paginated=True,
            delimiter=",",
            autofit=True,
            **kwargs)

    def _build_pagination_frame(self):
        """Build the frame containing the pagination widgets. This
        frame is only built if `pagination=True` when creating the
        widget.
        """
        pageframe = ttk.Frame(self)
        pageframe.pack(fill=X, anchor=N)

        ttk.Button(
            pageframe,
            text=MessageCatalog.translate("⎌"),
            command=self.reset_table,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT)

        ttk.Separator(pageframe, orient=VERTICAL).pack(side=RIGHT, padx=10)
        ttk.Checkbutton(pageframe, variable=self.autoscroll, text="Авто-прокрутка").pack(
            side=LEFT, fill=Y
        )
        ttk.Button(
            master=pageframe,
            text="»",
            command=self.goto_last_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)
        ttk.Button(
            master=pageframe,
            text="›",
            command=self.goto_next_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)

        ttk.Button(
            master=pageframe,
            text="‹",
            command=self.goto_prev_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)
        ttk.Button(
            master=pageframe,
            text="«",
            command=self.goto_first_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)


    def _build_pagination_frame(self):
        """Build the frame containing the pagination widgets. This
        frame is only built if `pagination=True` when creating the
        widget.
        """
        pageframe = ttk.Frame(self)
        pageframe.pack(fill=X, anchor=N)

        ttk.Button(
            pageframe,
            text=MessageCatalog.translate("⎌"),
            command=self.reset_table,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT)

        ttk.Separator(pageframe, orient=VERTICAL).pack(side=RIGHT, padx=10)
        ttk.Checkbutton(pageframe, variable=self.autoscroll, text="Авто-прокрутка").pack(
            side=LEFT, fill=Y
        )
        ttk.Button(
            master=pageframe,
            text="»",
            command=self.goto_last_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)
        ttk.Button(
            master=pageframe,
            text="›",
            command=self.goto_next_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)

        ttk.Button(
            master=pageframe,
            text="‹",
            command=self.goto_prev_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)
        ttk.Button(
            master=pageframe,
            text="«",
            command=self.goto_first_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)


def load():
    i = 0
    while True:
        meter.configure(subtext=f"Угол {i}")
        for i in range(10):
            root.after(1, lambda: meter.step(1))
            sleep(0.01)
        table.insert_row(values=[
            int(time()), meter.amountusedvar.get(), randint(1, 10), randint(1, 10)
        ])
        # if meter.table.autoscroll:
        root.after(10, lambda: table.goto_last_page())
        for i in range(10):
            if i % 2 == 0:
                root.after(10, lambda: meter.step(1))
                
                root.after(50, lambda: meter.step(1))
            else:
                root.after(10, lambda: meter.step(-1))
                root.after(50, lambda: meter.step(-1))
            sleep(0.2)

root = ttk.Window()


meter = CalibrationLoader(
    metersize=360,
    # arcrange=360,
    amounttotal=360,
    padding=5,
    amountused=0,
    metertype="full",
    subtext="miles per hour"
)
meter.pack()

table = CurParamTable(root,
    coldata=["Время", "Угол", "C1", "C2"]
    
)
        
table.pack()

# update the amount used directly
meter.configure(amountused = 0)

# update the amount used with another widget
entry = ttk.Entry(textvariable=meter.amountusedvar)
entry.pack(fill=X)


# update the subtext
meter.configure(subtext="loading...")
Thread(target=load, daemon=True).start()
root.mainloop()