from threading import Thread

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from time import sleep


def load():
    i = 0
    while True:
        meter.configure(subtext=f"Угол {i}")
        for i in range(10):
            app.after(1, lambda: meter.step(1))
            sleep(0.01)
        for i in range(10):
            if i % 2 == 0:
                app.after(10, lambda: meter.step(1))
                
                app.after(50, lambda: meter.step(1))
            else:
                app.after(10, lambda: meter.step(-1))
                app.after(50, lambda: meter.step(-1))
            sleep(0.2)

app = ttk.Window()

meter = ttk.Meter(
    metersize=360,
    arcrange=360,
    amounttotal=360,
    padding=5,
    amountused=0,
    metertype="semi",
    subtext="miles per hour",
    interactive=True,
)
meter.pack()

# update the amount used directly
meter.configure(amountused = 0)

# update the amount used with another widget
entry = ttk.Entry(textvariable=meter.amountusedvar)
entry.pack(fill=X)


# update the subtext
meter.configure(subtext="loading...")
Thread(target=load, daemon=True).start()
app.mainloop()