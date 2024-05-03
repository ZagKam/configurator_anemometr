import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from serial_ports import serial_ports
from get_version import get_version
from serialport import Serial
from all_parameters import all_params
from threading import Thread
import numpy as np
import serial
from sched import scheduler
from time import sleep


class Mutton(ttk.Button):
    ...



PORTS = {'port_uz':None,
             'port_js':None}

def open_ports_click(name_1:str):
    try:
        ComPort = serial.Serial(name_1, timeout=1)
        ComPort.baudrate = 19200
        return ComPort
    except serial.SerialException:
        print(f"Не удалось открыть порт COM: {name_1}. Проверьте подключение.")
        return None

# def on_entry_click(event, entry_widget, default_text):
#     if entry_widget.get() == default_text:
#         entry_widget.delete(0, "end")
#         entry_widget.config(fg='black')

# def on_focus_out(event, entry_widget, default_text):
#     if entry_widget.get() == "":
#         entry_widget.insert(0, default_text)
#         entry_widget.config(fg='grey')


def stream_param():
    name_param = [parameters_vel_text,parameters_angle_text,parameters_m12_text,parameters_m21_text,
                  parameters_m34_text,parameters_m43_text,parameters_t1_text,parameters_t2_text,
                  parameters_t3_text,parameters_t4_text]
    parameters = all_params(PORTS["port_uz"])
    for i, name in enumerate(name_param):
        name.delete("1.0", "end")
        
    for i, name in enumerate(name_param):
        name.insert("1.0", str(parameters[i]))
        

def uz_polling_cycle():
    while True:
        try:
            stream_param()
        except Exception as e:
            print("On polling cycle", e)
        sleep(1)


def start_compolling():
    port = open_ports_click(combo1.get())
    if port is None:
        raise ConnectionError("Can't open port")
    PORTS["port_uz"] = port
    display_version(get_version_call())
    start_get_params_thread()
    
    

def start_get_params_thread():
    Thread(target=uz_polling_cycle, daemon=True).start()
    

def display_version(version: str):
    version_variable.set(version)
    
    
def get_version_call() -> str:
    if PORTS["port_uz"] is None:
        raise ConnectionError("COM UZ is not opened")
    return str(get_version(PORTS["port_uz"]))
    
    
    
    

    

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, color='grey', placeholder="PLACEHOLDER", *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


def show_tooltip(text):
    tooltip_label.config(text=text)
    tooltip_label.place(relx=0.5, rely=0.5, anchor="center")

def hide_tooltip():
    tooltip_label.place_forget()

def create_tooltip(widget, text):
    widget.bind("<Enter>", lambda event: show_tooltip(text))
    widget.bind("<Leave>", lambda event: hide_tooltip())
    
    
    
# def display_text_out():
#     text = entry.get("1.0", "end-1c")  # Get text from input text area
#     output_text.delete("1.0", "end")   # Clear output text area
#     output_text.insert("1.0", text)    # Insert text into output text area

# def inv_text_out(default_text, output_text):
#     output_text.pack()
#     output_text.insert("1.0", default_text)
#     output_text.bind("<FocusIn>", lambda event: on_entry_click(event, output_text))
#     output_text.bind("<FocusOut>", lambda event: on_focus_out(event, output_text, default_text))




    
    
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

class ComportFrame(ttk.Frame):
    
    ...


class TkApp(tk.Tk):
        
    def __init__(self):
        super().__init__()
        
        self.title("Анемометр УЗ")

        # Установка размеров окна
        self.geometry("900x400")  # Ширина x Высота
        
        self.comport_frame = tk.Frame(self)
        self.entry_b_m_frame = tk.Frame(self)
        self.velocity_angle_loop_frame = tk.Frame(self)
        self.velocity_angle_const_frame = tk.Frame(self)
        self.oporn_signal_frame = tk.Frame(self)



    def label_naming(self):

        # Создаем метку для надписи над окном вывода
        comport_title_label = tk.Label(comport_frame)

        # Создаем метку для надписи над окном вывода
        entry_b_m_title_label = tk.Label(entry_b_m_frame)

        # Создаем метку для надписи над окном вывода
        velocity_angle_loop_title_label = tk.Label(velocity_angle_loop_frame)

        # Создаем метку для надписи над окном вывода
        velocity_angle_const_title_label = tk.Label(velocity_angle_const_frame)

        # Создаем метку для надписи над окном вывода
        oporn_signal_title_label = tk.Label(oporn_signal_frame)


    def build(self):

        # Создание Combobox
        values = serial_ports()
        combo1 = ttk.Combobox(comport_frame, values=values, width=22)

        combo1.set("Выберите COMport №1")

        # # Создание Combobox
        # values = serial_ports()
        # combo2 = ttk.Combobox(comport_frame, values=values, width=22)

        # combo2.set("Выберите COMport №2")

        # Создание кнопки и размещение с помощью grid
        button_open_port = Mutton(comport_frame, text="Открыть порты", command=lambda: open_ports_click(combo1.get()))


        # Создание кнопки и размещение с помощью grid
        button_close_port = Mutton(comport_frame, text="Закрыть порты", command=show_message)


        # Создание окна вывода версии
        info_label = tk.Label(root, text=f"dvdvvd")
        

        ##############################

        # Кнопка для начала записи
        input_m_b_button = Mutton(entry_b_m_frame, text="Запись", command=get_input)


        # Создание поля ввода и размещение с помощью grid
        default_text = 'Введите m'
        entry_m_b = EntryWithPlaceholder(entry_b_m_frame, placeholder=default_text)


        # окно вывода b
        output_m_b_text = tk.Text(entry_b_m_frame)
        output_m_b_text.configure(width=15, height=1)


        tooltip_label = ttk.Label(root, background="#ffffe0", relief="solid", borderwidth=1, wraplength=150)
        #tooltip_label.pack(ipadx=2, ipady=2, padx=10, pady=5)
        tooltip_label.config(font=("Helvetica", "8"))
        create_tooltip(output_m_b_text, "Отображение параметра b")

        ##################################

        # Кнопка для начала записи
        velocity_angle_loop_button = Mutton(velocity_angle_loop_frame, text="Начать цикл", command=get_input)


        # Создание поля ввода скорости для цикла
        default_text = 'Введите скорость'
        entry_velocity_angle = EntryWithPlaceholder(velocity_angle_loop_frame, placeholder=default_text)

        ##################################

        # Кнопка для определения значений определенной скороти и угла
        velocity_angle_const_button = Mutton(velocity_angle_const_frame, text="Найти", command=get_input)


        # Создание поля ввода скорости для определения одного значения
        default_text = 'Введите скорость'
        entry_velocity_const = EntryWithPlaceholder(velocity_angle_const_frame, placeholder=default_text)


        # Создание поля ввода угла для определения одного значения
        default_text = 'Введите угол'
        entry_angle_const = EntryWithPlaceholder(velocity_angle_const_frame, placeholder=default_text)


        ##################################

        # Кнопка для команды на запись опорных сигналов
        oporn_signal_button = Mutton(oporn_signal_frame, text="Запись опорных сигналов", command=get_input)


        # Создание окна для оповещения о завершении процесса записи опорных векторов
        info_label = tk.Label(oporn_signal_frame, text=f"здесь будет оповещение о завершении записи")


        ##################################

        comport_frame.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        entry_b_m_frame.grid(row=1, column=0, padx=10, pady=0, sticky='w')
        velocity_angle_loop_frame.grid(row=2, column=0, padx=10, pady=0, sticky='w')
        velocity_angle_const_frame.grid(row=3, column=0, padx=10, pady=0, sticky='w')
        oporn_signal_frame.grid(row=4, column=0, padx=10, pady=0, sticky='w')
        comport_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
        entry_b_m_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
        velocity_angle_loop_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
        velocity_angle_const_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
        oporn_signal_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
        combo1.grid(row=0, column=0, padx=10, pady=10)
        combo2.grid(row=0, column=1, padx=10, pady=10)
        button_open_port.grid(row=0, column=2, padx=10, pady=10)
        button_close_port.grid(row=0, column=3, padx=10, pady=10)
        info_label.grid(row=0, column=4, padx=10, pady=10)
        input_m_b_button.grid(row=1, column=0, padx=10, pady=1)
        entry_m_b.grid(row=1, column=1)
        output_m_b_text.grid(row=1, column=2, padx=20, pady=1)
        velocity_angle_loop_button.grid(row=1, column=0, padx=10, pady=1)
        entry_velocity_angle.grid(row=1, column=1)
        velocity_angle_const_button.grid(row=1, column=0, padx=10, pady=1)
        entry_velocity_const.grid(row=1, column=1)
        entry_angle_const.grid(row=1, column=2, padx=20, pady=1)
        oporn_signal_button.grid(row=1, column=0, padx=10, pady=1)
        info_label.grid(row=1, column=1, padx=10, pady=10)   
root = tk.Tk()
root.title("Анемометр УЗ")

# Установка размеров окна
root.geometry("800x450")  # Ширина x Высота


################################



# Создаем рамку для содержания выбора и подключения COMport
comport_frame = tk.Frame(root)

# Создаем рамку для отображения физических параметров в реальном времени
parameters_frame = tk.Frame(root)

# Создаем рамку для содержания команды записи m и b
entry_b_m_frame = tk.Frame(root)


# Создаем рамку для цикла записи скорости под разными углами (0,5,10,15)
velocity_angle_loop_frame = tk.Frame(root)


# Создаем рамку для записи определенного угла и скорости
velocity_angle_const_frame = tk.Frame(root)


# Создаем рамку для записи опорных сигналов
oporn_signal_frame = tk.Frame(root)

# Создаем рамку для отключения тока удержания
cur_off_frame = tk.Frame(root)

#################################


# Создаем метку для надписи над окном вывода
comport_title_label = tk.Label(comport_frame)

# Создаем метку для надписи над окном вывода
parameters_title_label = tk.Label(parameters_frame)

# Создаем метку для надписи над окном вывода
entry_b_m_title_label = tk.Label(entry_b_m_frame)


# Создаем метку для надписи над окном вывода
velocity_angle_loop_title_label = tk.Label(velocity_angle_loop_frame)


# Создаем метку для надписи над окном вывода
velocity_angle_const_title_label = tk.Label(velocity_angle_const_frame)


# Создаем метку для надписи над окном вывода
oporn_signal_title_label = tk.Label(oporn_signal_frame)


# Создаем метку для надписи над окном вывода
cur_off_title_label = tk.Label(cur_off_frame)


###################################


# Создание Combobox
values = serial_ports()
combo1 = ttk.Combobox(comport_frame, values=values, width=22)

combo1.set("Выберите COMport №1")

# Создание Combobox
values = serial_ports()
combo2 = ttk.Combobox(comport_frame, values=values, width=22)

combo2.set("Выберите COMport №2")

version_variable = tk.StringVar()
# Создание кнопки и размещение с помощью grid
button_open_port = Mutton(comport_frame, 
                          text="Открыть порты", 
                          command=start_compolling)# print(get_version(open_ports_click(combo1.get()))))


# Создание кнопки и размещение с помощью grid
button_close_port = Mutton(comport_frame, text="Закрыть порты", command=show_message)


# Создание окна вывода версии
info_vers_label = tk.Label(comport_frame, textvariable=version_variable)
  

##############################

# окно вывода скорости
vel_label = tk.Label(parameters_frame, text="Отображение скорости ветра")

parameters_vel_text = tk.Text(parameters_frame)
parameters_vel_text.configure(width=15, height=1)

# окно вывода угла
angle_label = tk.Label(parameters_frame, text="Отображение угла")

parameters_angle_text = tk.Text(parameters_frame)
parameters_angle_text.configure(width=15, height=1)


# окно вывода m12
m12_label = tk.Label(parameters_frame, text="Отображение m12")

parameters_m12_text = tk.Text(parameters_frame)
parameters_m12_text.configure(width=15, height=1)


# окно вывода m21
m21_label = tk.Label(parameters_frame, text="Отображение m21")

parameters_m21_text = tk.Text(parameters_frame)
parameters_m21_text.configure(width=15, height=1)


# окно вывода m34
m34_label = tk.Label(parameters_frame, text="Отображение m34")

parameters_m34_text = tk.Text(parameters_frame)
parameters_m34_text.configure(width=15, height=1)


# окно вывода m43
m43_label = tk.Label(parameters_frame, text="Отображение m43")

parameters_m43_text = tk.Text(parameters_frame)
parameters_m43_text.configure(width=15, height=1)



# окно вывода t1
t1_label = tk.Label(parameters_frame, text="Отображение t1")

parameters_t1_text = tk.Text(parameters_frame)
parameters_t1_text.configure(width=15, height=1)



# окно вывода t2
t2_label = tk.Label(parameters_frame, text="Отображение t2")

parameters_t2_text = tk.Text(parameters_frame)
parameters_t2_text.configure(width=15, height=1)




# окно вывода t3
t3_label = tk.Label(parameters_frame, text="Отображение t3")

parameters_t3_text = tk.Text(parameters_frame)
parameters_t3_text.configure(width=15, height=1)




# окно вывода t4
t4_label = tk.Label(parameters_frame, text="Отображение t4")

parameters_t4_text = tk.Text(parameters_frame)
parameters_t4_text.configure(width=15, height=1)



##############################

# Кнопка для начала записи
input_m_b_button = Mutton(entry_b_m_frame, text="Запись m", command=get_input)


# Создание поля ввода и размещение с помощью grid
default_text = 'Введите m'
entry_m_b = EntryWithPlaceholder(entry_b_m_frame, placeholder=default_text)


# окно вывода b
output_m_b_text = tk.Text(entry_b_m_frame)
output_m_b_text.configure(width=15, height=1)


tooltip_label = ttk.Label(root, background="#ffffe0", relief="solid", borderwidth=1, wraplength=150)
#tooltip_label.pack(ipadx=2, ipady=2, padx=10, pady=5)
tooltip_label.config(font=("Helvetica", "8"))
create_tooltip(output_m_b_text, "Отображение параметра b")

##################################

# Кнопка для начала записи
velocity_angle_loop_button = Mutton(velocity_angle_loop_frame, text="Начать цикл", command=get_input)


# Создание поля ввода скорости для цикла
default_text = 'Введите скорость'
entry_velocity_angle = EntryWithPlaceholder(velocity_angle_loop_frame, placeholder=default_text)

# Создание окна для оповещения о завершении процесса записи опорных векторов
velocity_angle_loop_info = tk.Label(velocity_angle_loop_frame, text=f"инофрмация о том какой сейчас угол")

##################################

# Кнопка для определения значений определенной скороти и угла
velocity_angle_const_button = Mutton(velocity_angle_const_frame, text="Найти с1,с2", command=get_input)


# Создание поля ввода скорости для определения одного значения
default_text = 'Введите скорость'
entry_velocity_const = EntryWithPlaceholder(velocity_angle_const_frame, placeholder=default_text)


# Создание поля ввода угла для определения одного значения
default_text = 'Введите угол'
entry_angle_const = EntryWithPlaceholder(velocity_angle_const_frame, placeholder=default_text)

# окно вывода b
output_c1_c2_text = tk.Text(velocity_angle_const_frame)
output_c1_c2_text.configure(width=15, height=1)


tooltip_label = ttk.Label(root, background="#ffffe0", relief="solid", borderwidth=1, wraplength=150)
#tooltip_label.pack(ipadx=2, ipady=2, padx=10, pady=5)
tooltip_label.config(font=("Helvetica", "8"))
create_tooltip(output_c1_c2_text, "Отображение параметров с1, с2")


##################################

# Кнопка для команды на запись опорных сигналов
oporn_signal_button = Mutton(oporn_signal_frame, text="Запись опорных сигналов", command=get_input)


# Создание окна для оповещения о завершении процесса записи опорных векторов
end_write_oporn = tk.Label(oporn_signal_frame, text=f"здесь будет оповещение о завершении записи")

##################################

# Кнопка для оставновки тока удержания 
cur_off_button = Mutton(cur_off_title_label, text="Отключение тока удержания", command=get_input)

# Создание окна для оповещения о завершении процесса записи опорных векторов
cur_off_info = tk.Label(cur_off_title_label, text=f"здесь будет оповещение об отключении тока")

##################################


comport_frame.grid(row=0, column=0, padx=10, pady=5, sticky='w')
parameters_frame.grid(row=1, column=0, padx=10, pady=5, sticky='w')
entry_b_m_frame.grid(row=2, column=0, padx=10, pady=0, sticky='w')
velocity_angle_loop_frame.grid(row=3, column=0, padx=10, pady=0, sticky='w')
velocity_angle_const_frame.grid(row=4, column=0, padx=10, pady=0, sticky='w')
oporn_signal_frame.grid(row=5, column=0, padx=10, pady=0, sticky='w')
cur_off_frame.grid(row=6, column=0, padx=10, pady=0, sticky='w')
comport_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
entry_b_m_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
velocity_angle_loop_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
velocity_angle_const_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
oporn_signal_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
cur_off_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
combo1.grid(row=0, column=0, padx=10, pady=10)
combo2.grid(row=0, column=1, padx=10, pady=10)
button_open_port.grid(row=0, column=2, padx=10, pady=10)
button_close_port.grid(row=0, column=3, padx=10, pady=10)
info_vers_label.grid(row=0, column=4, padx=0, pady=0)

parameters_vel_text.grid(row=1, column=0, padx=0, pady=0)
vel_label.grid(row=0, column=0)
parameters_angle_text.grid(row=1, column=1, padx=0, pady=0)
angle_label.grid(row=0, column=1)
parameters_m12_text.grid(row=1, column=2, padx=15, pady=0)
m12_label.grid(row=0, column=2)
parameters_m21_text.grid(row=1, column=3, padx=15, pady=0)
m21_label.grid(row=0, column=3)
parameters_m34_text.grid(row=1, column=4, padx=0, pady=0)
m34_label.grid(row=0, column=4)
parameters_m43_text.grid(row=3, column=0, padx=0, pady=0)
m43_label.grid(row=2, column=0)
parameters_t1_text.grid(row=3, column=1, padx=0, pady=0)
t1_label.grid(row=2, column=1)
parameters_t2_text.grid(row=3, column=2, padx=0, pady=0)
t2_label.grid(row=2, column=2)
parameters_t3_text.grid(row=3, column=3, padx=0, pady=0)
t3_label.grid(row=2, column=3)
parameters_t4_text.grid(row=3, column=4, padx=0, pady=0)
t4_label.grid(row=2, column=4)

input_m_b_button.grid(row=3, column=0, padx=10, pady=1)
entry_m_b.grid(row=3, column=1)
output_m_b_text.grid(row=3, column=2, padx=20, pady=1) 
velocity_angle_loop_button.grid(row=1, column=0, padx=10, pady=1)
entry_velocity_angle.grid(row=1, column=1)
velocity_angle_loop_info.grid(row=1, column=2)
velocity_angle_const_button.grid(row=1, column=0, padx=10, pady=1)
entry_velocity_const.grid(row=1, column=1)
entry_angle_const.grid(row=1, column=2, padx=20, pady=1)
output_c1_c2_text.grid(row=1, column=3, padx=0, pady=1)
oporn_signal_button.grid(row=1, column=0, padx=10, pady=1)
end_write_oporn.grid(row=1, column=1, padx=10, pady=1)
cur_off_button.grid(row=1, column=1, padx=0, pady=10)  
cur_off_info.grid(row=1, column=2, padx=0, pady=10) 
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