from typing import Literal, Tuple
from time import sleep
from threading import Thread
from threading import Event
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import serial

from serial_ports import serial_ports
from get_version import get_version
from serialport import Serial
from all_parameters import all_params
from set_m_b_get_b import set_m
from calibr_koef import calibration_koef
from oporn_signal import entry_oporn_signal
from calibration_loop import calibration_loop
from five_degrees import initial_calibration


stop_thread = True


class Mutton(ttk.Button):
    ...


PORTS = {'port_uz':None,
         'port_js':None}


def open_ports_click(name_1:str, name_2: str) -> Tuple[Serial, Serial]:
    try:
        global stop_thread
        stop_thread = True
        ComPort1 = Serial(name_1, 19200, timeout=1)
        ComPort2 = Serial(name_2, 38400, timeout=1)
        return ComPort1, ComPort2
    except serial.SerialException:
        print(f"Не удалось открыть порт COM: {name_1}. Проверьте подключение.")
        return None


def stream_param():
    try:
        parameters = all_params(PORTS["port_uz"])
    except Exception as e:
        print("stream_param", e)
        raise
    for i, name in enumerate(NAME_PARAM):
        name.delete("1.0", "end")
        
    for i, name in enumerate(NAME_PARAM):
        name.insert("1.0", str(parameters[i]))
        

def uz_polling_cycle():
    while stop_thread:
        try:
            stream_param()
        except ValueError:
            pass
        except Exception as e:
            print("On polling cycle", e)
            
            messagebox.showerror(f"{e}")
            break
        sleep(1)


def start_compolling():
    """Open two com ports. Start displaying current parameters
    in a separate thread

    :raises ConnectionError: _description_
    """
    port_uz, port_js = open_ports_click(combo1.get(), combo2.get())
    if any((port_uz is None, 
            port_js is None)):
        raise ConnectionError("Can't open port")
    PORTS["port_uz"] = port_uz
    PORTS["port_js"] = port_js
    initial_calibration(port_js)
    display_version(get_version_call())
    start_get_params_thread()
    

def start_get_params_thread():
    global thread_param
    thread_param = Thread(target=uz_polling_cycle, daemon=True)
    thread_param.start()


def display_version(version: str):
    version_variable.set(f"FW: {version}")

        
def get_version_call() -> str:
    if PORTS["port_uz"] is None:
        raise ConnectionError("COM UZ is not opened")
    return str(get_version(PORTS["port_uz"]))
    
    
def close_ports_clicks():
    try:
        global stop_thread
        stop_thread = False
        PORTS["port_uz"].close()
        #thread_param.join()
        for i, name in enumerate(NAME_PARAM):
            name.delete("1.0", "end")
    except serial.SerialException:
        print(f"Что-то пошло не так при закрытии Com-портов")


def _write_m():
    
    value = set_m(PORTS["port_uz"], entry_m_b.get())
    output_m_b_text.delete("1.0", "end")
    output_m_b_text.insert("1.0", str(value))

    
def write_m():
    Thread(target=_write_m, daemon=True).start()
    

def _find_c1_c2():
    
    value = calibration_koef(PORTS["port_uz"], entry_velocity_const.get(), entry_angle_const.get())
    output_c1_c2_text.delete("1.0", "end")
    output_c1_c2_text.insert("1.0", (str(value[0]) +','+ str(value[1])))
    
    
def find_c1_c2():
    Thread(target=_find_c1_c2, daemon=True).start()
    

def _write_oporn_sign(end_event: Event):
    entry_oporn_signal(PORTS["port_uz"])
    all_block('normal')
    end_event.clear()
    end_write_oporn_var.set('Запись завершена')
    messagebox.showinfo("", "Внимание! Переподключите устройство.")


def write_oporn_sign():
    all_block('disabled')
    end_event = Event()
    end_event.set()
    Thread(target=_write_oporn_sign, args=(end_event,), daemon=True).start()
    Thread(target=loader, args=(end_event,), daemon=True).start()
    

def loader(end_event):
    while True:
        for i in ["\\", "|", "/", "—"]:
            sleep(1)
            if not end_event.is_set():
                return
            end_write_oporn_var.set('Идет запись опорных сигналов ' + i)
    

def all_block(state: Literal["disabled", "normal"]):
    for i in ALL_BUTTONS:
        i: tk.Button
        i['state'] = state


def start_calibration_cycle():
    """
    Start calibration cycle in a separate thread
    """
    Thread(target=_start_calibration_cycle, daemon=True, 
           name="CalibrationThread").start()


def _start_calibration_cycle():
    wind_velocity = entry_velocity_angle.get().strip()
    if not wind_velocity.isdigit():
        messagebox.showwarning("Ошибка ввода", "Введена некорректная скорость")
        return
    wind_velocity = int(wind_velocity)
    PORTS["port_uz"].enter_calibration()
    calibration_loop(ui_update, 
                     wind_velocity, PORTS["port_uz"],
                     PORTS["port_js"])
    PORTS["port_uz"].exit_calibration()


def ui_update(wind_velocity: int, angle: int):
    current_angle.set(f"{wind_velocity}м/c,  {angle}"+b'\xc2\xb0'.decode("utf8") )


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


# class TkApp(tk.Tk):
        
#     def __init__(self):
#         super().__init__()
        
#         self.title("Анемометр УЗ")

#         # Установка размеров окна
#         self.geometry("900x400")  # Ширина x Высота
        
#         self.comport_frame = tk.Frame(self)
#         self.entry_b_m_frame = tk.Frame(self)
#         self.velocity_angle_loop_frame = tk.Frame(self)
#         self.velocity_angle_const_frame = tk.Frame(self)
#         self.oporn_signal_frame = tk.Frame(self)



#     def label_naming(self):

#         # Создаем метку для надписи над окном вывода
#         comport_title_label = tk.Label(comport_frame)

#         # Создаем метку для надписи над окном вывода
#         entry_b_m_title_label = tk.Label(entry_b_m_frame)

#         # Создаем метку для надписи над окном вывода
#         velocity_angle_loop_title_label = tk.Label(velocity_angle_loop_frame)

#         # Создаем метку для надписи над окном вывода
#         velocity_angle_const_title_label = tk.Label(velocity_angle_const_frame)

#         # Создаем метку для надписи над окном вывода
#         oporn_signal_title_label = tk.Label(oporn_signal_frame)


#     def build(self):

#         # Создание Combobox
#         values = serial_ports()
#         combo1 = ttk.Combobox(comport_frame, values=values, width=22)

#         combo1.set("Выберите COMport №1")

#         # # Создание Combobox
#         # values = serial_ports()
#         # combo2 = ttk.Combobox(comport_frame, values=values, width=22)

#         # combo2.set("Выберите COMport №2")

#         # Создание кнопки и размещение с помощью grid
#         button_open_port = Mutton(comport_frame, text="Открыть порты", command=lambda: open_ports_click(combo1.get()))


#         # Создание кнопки и размещение с помощью grid
#         button_close_port = Mutton(comport_frame, text="Закрыть порты", command=show_message)


#         # Создание окна вывода версии
#         info_label = tk.Label(root, text=f"dvdvvd")
        

#         ##############################

#         # Кнопка для начала записи
#         input_m_b_button = Mutton(entry_b_m_frame, text="Запись", command=get_input)


#         # Создание поля ввода и размещение с помощью grid
#         default_text = 'Введите m'
#         entry_m_b = EntryWithPlaceholder(entry_b_m_frame, placeholder=default_text)


#         # окно вывода b
#         output_m_b_text = tk.Text(entry_b_m_frame)
#         output_m_b_text.configure(width=15, height=1)


#         tooltip_label = ttk.Label(root, background="#ffffe0", relief="solid", borderwidth=1, wraplength=150)
#         #tooltip_label.pack(ipadx=2, ipady=2, padx=10, pady=5)
#         tooltip_label.config(font=("Helvetica", "8"))
#         create_tooltip(output_m_b_text, "Отображение параметра b")

#         ##################################

#         # Кнопка для начала записи
#         velocity_angle_loop_button = Mutton(velocity_angle_loop_frame, text="Начать цикл", command=get_input)


#         # Создание поля ввода скорости для цикла
#         default_text = 'Введите скорость'
#         entry_velocity_angle = EntryWithPlaceholder(velocity_angle_loop_frame, placeholder=default_text)

#         ##################################

#         # Кнопка для определения значений определенной скороти и угла
#         velocity_angle_const_button = Mutton(velocity_angle_const_frame, text="Найти", command=get_input)


#         # Создание поля ввода скорости для определения одного значения
#         default_text = 'Введите скорость'
#         entry_velocity_const = EntryWithPlaceholder(velocity_angle_const_frame, placeholder=default_text)


#         # Создание поля ввода угла для определения одного значения
#         default_text = 'Введите угол'
#         entry_angle_const = EntryWithPlaceholder(velocity_angle_const_frame, placeholder=default_text)


#         ##################################

#         # Кнопка для команды на запись опорных сигналов
#         oporn_signal_button = Mutton(oporn_signal_frame, text="Запись опорных сигналов", command=get_input)


#         # Создание окна для оповещения о завершении процесса записи опорных векторов
#         info_label = tk.Label(oporn_signal_frame, text=f"здесь будет оповещение о завершении записи")


#         ##################################

#         comport_frame.grid(row=0, column=0, padx=10, pady=5, sticky='w')
#         entry_b_m_frame.grid(row=1, column=0, padx=10, pady=0, sticky='w')
#         velocity_angle_loop_frame.grid(row=2, column=0, padx=10, pady=0, sticky='w')
#         velocity_angle_const_frame.grid(row=3, column=0, padx=10, pady=0, sticky='w')
#         oporn_signal_frame.grid(row=4, column=0, padx=10, pady=0, sticky='w')
#         comport_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
#         entry_b_m_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
#         velocity_angle_loop_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
#         velocity_angle_const_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
#         oporn_signal_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))
#         combo1.grid(row=0, column=0, padx=10, pady=10)
#         combo2.grid(row=0, column=1, padx=10, pady=10)
#         button_open_port.grid(row=0, column=2, padx=10, pady=10)
#         button_close_port.grid(row=0, column=3, padx=10, pady=10)
#         info_label.grid(row=0, column=4, padx=10, pady=10)
#         input_m_b_button.grid(row=1, column=0, padx=10, pady=1)
#         entry_m_b.grid(row=1, column=1)
#         output_m_b_text.grid(row=1, column=2, padx=20, pady=1)
#         velocity_angle_loop_button.grid(row=1, column=0, padx=10, pady=1)
#         entry_velocity_angle.grid(row=1, column=1)
#         velocity_angle_const_button.grid(row=1, column=0, padx=10, pady=1)
#         entry_velocity_const.grid(row=1, column=1)
#         entry_angle_const.grid(row=1, column=2, padx=20, pady=1)
#         oporn_signal_button.grid(row=1, column=0, padx=10, pady=1)
#         info_label.grid(row=1, column=1, padx=10, pady=10)   
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
button_close_port = Mutton(comport_frame, text="Закрыть порты", command=close_ports_clicks)


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
input_m_b_button = Mutton(entry_b_m_frame, text="Запись m", command=write_m)


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
velocity_angle_loop_button = Mutton(
    velocity_angle_loop_frame, text="Начать цикл", command=start_calibration_cycle)


# Создание поля ввода скорости для цикла
default_text = 'Введите скорость'
entry_velocity_angle = EntryWithPlaceholder(velocity_angle_loop_frame, placeholder=default_text)

current_angle = tk.StringVar(velocity_angle_loop_frame)
# Создание окна для оповещения о завершении процесса записи опорных векторов
velocity_angle_loop_info = tk.Label(velocity_angle_loop_frame, 
                                    textvariable=current_angle,
                                    text=f"информация о том, какой сейчас угол")

##################################

# Кнопка для определения значений определенной скороти и угла
velocity_angle_const_button = Mutton(velocity_angle_const_frame, text="Найти с1,с2", command=find_c1_c2)


# Создание поля ввода скорости для определения одного значения
default_text = 'Введите скорость'
entry_velocity_const = EntryWithPlaceholder(velocity_angle_const_frame, placeholder=default_text)


# Создание поля ввода угла для определения одного значения
default_text = 'Введите угол'
entry_angle_const = EntryWithPlaceholder(velocity_angle_const_frame, placeholder=default_text)

# окно вывода c1,c2
output_c1_c2_text = tk.Text(velocity_angle_const_frame)
output_c1_c2_text.configure(width=15, height=1)


tooltip_label = ttk.Label(root, background="#ffffe0", relief="solid", borderwidth=1, wraplength=150)
#tooltip_label.pack(ipadx=2, ipady=2, padx=10, pady=5)
tooltip_label.config(font=("Helvetica", "8"))
create_tooltip(output_c1_c2_text, "Отображение параметров с1, с2")


##################################

# Кнопка для команды на запись опорных сигналов
oporn_signal_button = Mutton(oporn_signal_frame, text="Запись опорных сигналов", command=write_oporn_sign)


# Создание окна для оповещения о завершении процесса записи опорных векторов
end_write_oporn_var = tk.StringVar(oporn_signal_frame, f"здесь будет оповещение о завершении записи")
end_write_oporn = tk.Label(oporn_signal_frame, textvariable=end_write_oporn_var)

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



NAME_PARAM = [parameters_vel_text,parameters_angle_text,parameters_m12_text,parameters_m21_text,
                parameters_m34_text,parameters_m43_text,parameters_t1_text,parameters_t2_text,
                parameters_t3_text,parameters_t4_text]
ALL_BUTTONS = [button_open_port,button_close_port,
               input_m_b_button,velocity_angle_loop_button,
               velocity_angle_const_button,oporn_signal_button,
               cur_off_button]
root.mainloop()