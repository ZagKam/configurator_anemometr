import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from serial_ports import serial_ports
from get_version import get_version
from serialport import Serial
import threading
import numpy as np


class Mutton(ttk.Button):
    ...



PORTS = {'port_1':None,
             'port_2':None}

def open_ports_click(name_1:str, name_2:str, *args):
    PORTS["port_1"] = Serial(name_1,baudrate = 19200, bytesize = 8)
    PORTS["port_2"] = Serial(name_2,baudrate = 19200, bytesize = 8)









def on_entry_click(event, entry_widget):
    if entry_widget.get() == default_text:
        entry_widget.delete(0, "end")
        entry_widget.config(fg='black')

def on_focus_out(event, entry_widget, default_text):
    if entry_widget.get() == "":
        entry_widget.insert(0, default_text)
        entry_widget.config(fg='grey')


def show_tooltip(text):
    tooltip_label.config(text=text)
    tooltip_label.place(relx=0.5, rely=0.5, anchor="center")

def hide_tooltip():
    tooltip_label.place_forget()

def create_tooltip(widget, text):
    widget.bind("<Enter>", lambda event: show_tooltip(text))
    widget.bind("<Leave>", lambda event: hide_tooltip())
    
    
    
def display_text_out():
    text = entry.get("1.0", "end-1c")  # Get text from input text area
    output_text.delete("1.0", "end")   # Clear output text area
    output_text.insert("1.0", text)    # Insert text into output text area

def inv_text_out(default_text, output_text):
    output_text.pack()
    output_text.insert("1.0", default_text)
    output_text.bind("<FocusIn>", lambda event: on_entry_click(event, output_text))
    output_text.bind("<FocusOut>", lambda event: on_focus_out(event, output_text, default_text))



def vers():
    # version = np.random.randint(0, 200)
    version = get_version
    info = f"Версия: {version}"
    info_label.config(text=info)
    
    
def show_message():
    messagebox.showinfo("Сообщение", "Вы нажали кнопку!")

def get_input():
    messagebox.showinfo("", 'нажали кнопку')

def check_state():
    if var.get() == 1:
        messagebox.showinfo("Чекбокс", "Чекбокс отмечен")
    else:
        messagebox.showinfo("Чекбокс", "Чекбокс не отмечен")

# Создание главного окна
root = tk.Tk()
root.title("Анемометр УЗ")

# Установка размеров окна
root.geometry("900x300")  # Ширина x Высота


################################





# Создаем рамку для содержания выбора и подключения COMport
comport_frame = tk.Frame(root)
comport_frame.grid(row=0, column=0, padx=10, pady=5, sticky='w')

# Создаем рамку для содержания команды записи m и b
entry_b_m_frame = tk.Frame(root)
entry_b_m_frame.grid(row=1, column=0, padx=10, pady=0, sticky='w')

#################################






# Создаем метку для надписи над окном вывода
comport_title_label = tk.Label(comport_frame)
comport_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))


# Создаем метку для надписи над окном вывода
entry_b_m_title_label = tk.Label(entry_b_m_frame)
entry_b_m_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))

###################################





# Создание Combobox
values = serial_ports()
combo1 = ttk.Combobox(comport_frame, values=values, width=22)
combo1.grid(row=0, column=0, padx=10, pady=10)
combo1.set("Выберите COMport №1")

# Создание Combobox
values = serial_ports()
combo2 = ttk.Combobox(comport_frame, values=values, width=22)
combo2.grid(row=0, column=1, padx=10, pady=10)
combo2.set("Выберите COMport №2")

# Создание кнопки и размещение с помощью grid
button_open_port = Mutton(comport_frame, text="Открыть порты", command=lambda event: open_ports_click(combo1.get(), combo2.get()))
button_open_port.grid(row=0, column=2, padx=10, pady=10)


# Создание кнопки и размещение с помощью grid
button_close_port = Mutton(comport_frame, text="Закрыть порты", command=show_message)
button_close_port.grid(row=0, column=3, padx=10, pady=10)


# Создание окна вывода версии
info_label = tk.Label(root, text=f"")
info_label.grid(row=0, column=4, padx=10, pady=10)  
vers()
##############################
# Кнопка для начала записи
input_m_b_button = Mutton(entry_b_m_frame, text="Запись", command=get_input)
input_m_b_button.grid(row=1, column=0, padx=10, pady=1)

# Создание поля ввода и размещение с помощью grid
default_text = 'Введите m'
entry_m_b = tk.Entry(entry_b_m_frame, fg='grey')
entry_m_b.insert(0, default_text)
entry_m_b.bind("<FocusIn>", lambda event: on_entry_click(event, entry_m_b))
entry_m_b.bind("<FocusOut>", lambda event: on_focus_out(event, entry_m_b, default_text))
entry_m_b.grid(row=1, column=1)

# окно вывода b
output_m_b_text = tk.Text(entry_b_m_frame)
output_m_b_text.configure(width=15, height=1)
output_m_b_text.grid(row=1, column=2, padx=20, pady=1)

tooltip_label = ttk.Label(root, background="#ffffe0", relief="solid", borderwidth=1, wraplength=150)
#tooltip_label.pack(ipadx=2, ipady=2, padx=10, pady=5)
tooltip_label.config(font=("Helvetica", "8"))
create_tooltip(output_m_b_text, "Отображение параметра b")
##################################



# # Создание кнопки и размещение с помощью grid
# button = tk.Button(root, text="Нажми меня", command=show_message)
# button.grid(row=5, column=0, padx=10, pady=10)

# # Создание поля ввода и размещение с помощью grid
# entry = tk.Entry(root)
# entry.grid(row=1, column=0, padx=10, pady=10)

# # Создание кнопки для получения данных из поля ввода и размещение с помощью grid
# input_button = tk.Button(root, text="Получить данные", command=get_input)
# input_button.grid(row=2, column=0, padx=10, pady=10)

# # Создание чекбокса и размещение с помощью grid
# var = tk.IntVar()
# checkbox = tk.Checkbutton(root, text="Отметить", variable=var, command=check_state)
# checkbox.grid(row=3, column=0, padx=10, pady=10)

# # Создание Combobox
# values = ["Вариант 1", "Вариант 2", "Вариант 3"]
# combo = ttk.Combobox(root, values=values)
# combo.grid(row=4, column=0, padx=10, pady=10)
# combo.set("Выберите вариант")



# Запуск главного цикла обработки событий
root.mainloop()