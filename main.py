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
from current_off import current_off
from program_logger import logger

stop_thread = True


class Mutton(ttk.Button):
    ...


PORTS = {'port_uz':None,
         'port_js':None}


def open_ports_click(name_1:str, name_2: str) -> Tuple[Serial, Serial]:
    try:
        global stop_thread
        stop_thread = True
        try:
            ComPort1 = Serial(name_1, 19200, timeout=1)
        except Exception as e:
            
            logger.warning(f"Не удалось открыть порт {name_1}: Проверьте подключение.")
            raise serial.SerialException(f"Не удалось открыть порт {name_1}: Проверьте подключение.")
        try:
            ComPort2 = Serial(name_2, 38400, timeout=1)
        except Exception as e:
            logger.warning(f"Не удалось открыть порт {name_2}: Проверьте подключение.")
            ComPort1.close()
            raise serial.SerialException(f"Не удалось открыть порт {name_2}: Проверьте подключение.")
        return ComPort1, ComPort2
    except serial.SerialException as e:
        raise e

def fill_combobox(e):
    ports = serial_ports()
    e.widget["values"] = ports


def stream_param():
    try:
        parameters = all_params(PORTS["port_uz"])
    except Exception as e:
        logger.warning(f"{e}")
        raise e
    for i, name in enumerate(NAME_PARAM):
        name.delete("1.0", "end")
        
    for i, name in enumerate(NAME_PARAM):
        name.insert("1.0", str(parameters[i]))
        

def uz_polling_cycle():
    while stop_thread:
        try:
            stream_param()
        except ValueError as e:
            logger.debug(f"{e}")
            pass
        except Exception as e:
            logger.error(f"UZ polling cycle break {e}")
            
            messagebox.showerror(
                "Ошибка",
                (f"В цикле опроса анемоментра возникла ошибка. "
                f"Для перезапуска закройте порт и откройте его повторно. \n{e}"))
            break
        sleep(1)


def start_compolling():
    """Open two com ports. Start displaying current parameters
    in a separate thread

    :raises ConnectionError: _description_
    """
    try:
        port_uz, port_js = open_ports_click(combo1.get(), combo2.get())
        logger.debug(f"UZ polling was started on {port_uz}")
    except Exception as e:
        logger.info(f"Couldn't connect to serial {e}")
        messagebox.showerror("Ошибка подключения", e)
        return
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
    logger.debug(f"UZ FW version is {version}")
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
        PORTS["port_js"].close()
        combo2.set("Выберете COMport №2")
        #thread_param.join()
        for i, name in enumerate(NAME_PARAM):
            name.delete("1.0", "end")
        logger.info("COM ports were closed")
    except serial.SerialException as e:
        logger.exception(e)


def _write_m():
    m_value = entry_m_b.get().strip()
    if not m_value.isdigit():
        logger.debug(f"Incorrect input for {m_value=}")
        messagebox.showwarning("Неверный ввод", "Введено некорректное значение")
        return
    value = set_m(PORTS["port_uz"], entry_m_b.get())
    logger.info(f"For m_value {value=} is set")
    output_m_b_text.delete("1.0", "end")
    output_m_b_text.insert("1.0", str(value))

    
def write_m():
    Thread(target=_write_m, daemon=True).start()
    

def _find_c1_c2():
    angle = entry_angle_const.get().strip()
    velocity = entry_velocity_const.get()
    if not angle.isdigit() or int(angle) > 359:
        messagebox.showwarning("Ошибка ввода", "Введен некорректный угол")
        return
    if not velocity.isdigit():
        messagebox.showwarning("Ошибка ввода", "Введена некорректная скорость")
        return
    logger.debug(f"Function was called with {angle=} {velocity=}")
    value = calibration_koef(PORTS["port_uz"], entry_velocity_const.get(), entry_angle_const.get())
    if value == -1:
        logger.info("UZ didn't respond")
        messagebox.showwarning("Неверный ответ", "Прибор не ответил")
    logger.debug(f"New {value=} was set")
    output_c1_c2_text.delete("1.0", "end")
    output_c1_c2_text.insert("1.0", (str(value[0]) +','+ str(value[1])))
    
    
def find_c1_c2():
    Thread(target=_find_c1_c2, daemon=True).start()
    

def _write_oporn_sign(end_event: Event):
    entry_oporn_signal(PORTS["port_uz"])
    logger.debug(f"UZ oporn signals setting has started")
    all_block('normal')
    end_event.clear()
    end_write_oporn_var.set('Запись завершена')
    logger.debug("Oporn signals settings is done")
    messagebox.showinfo(
        "Уведомление", 
        "Запись завершена. Снимите питание с датчика и подключите снова.")


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
    status.set("Калибровка началась")
    Thread(target=_start_calibration_cycle, daemon=True, 
           name="CalibrationThread").start()


def _start_calibration_cycle():
    wind_velocity = entry_velocity_angle.get().strip()
    if not wind_velocity.isdigit():
        messagebox.showwarning("Ошибка ввода", "Введена некорректная скорость")
        return
    wind_velocity = int(wind_velocity)
    PORTS["port_uz"].enter_calibration()
    initial_calibration(PORTS["port_js"])
    calibration_loop(ui_update, 
                     wind_velocity, PORTS["port_uz"],
                     PORTS["port_js"])
    PORTS["port_uz"].exit_calibration()
    status.set("Калибровка завершена")
    messagebox.showinfo("Информация", "Цикл калибровки завершён")
    current_angle.set("")


def ui_update(wind_velocity: int, angle: int):
    current_angle.set(f"{wind_velocity}м/c,  {angle}"+b'\xc2\xb0'.decode("utf8") )


def _cur_off(end_event: Event):
    if current_off(PORTS["port_js"]):    
        end_write_curr_off_var.set('Запись завершена')
        messagebox.showinfo("Уведомение", 
                            ("Удержание двигателя отключено. Для продолжения работы "
                             "отключите от него питание и подключите снова"))
    all_block('normal')
    end_event.clear()

def cur_off():
    all_block('disabled')
    end_event = Event()
    end_event.set()
    Thread(target=_cur_off, args=(end_event,), daemon=True).start()
    Thread(target=loader_curr, args=(end_event,), daemon=True).start()

def loader_curr(end_event):
    while True:
        for i in ["\\", "|", "/", "—"]:
            sleep(1)
            if not end_event.is_set():
                return
            end_write_curr_off_var.set('Отключение тока ' + i)


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


# def show_tooltip(text):
#     tooltip_label.config(text=text)
#     tooltip_label.place(relx=0.5, rely=0.5, anchor="center")

# def hide_tooltip():
#     tooltip_label.place_forget()

# def create_tooltip(widget, text):
#     widget.bind("<Enter>", lambda event: show_tooltip(text))
#     widget.bind("<Leave>", lambda event: hide_tooltip())
    
    
    





    
    
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


root = tk.Tk()
root.title("Анемометр УЗ v.0.0.1b")

# Установка размеров окна
root.geometry("1000x300")  # Ширина x Высота


################################



# Создаем рамку для содержания выбора и подключения COMport
comport_frame = tk.Frame(root)

com_port_frame_separator = ttk.Separator(root, orient=tk.VERTICAL)

# Создаем рамку для отображения физических параметров в реальном времени
main_interaction_frame = tk.Frame(root)
parameters_frame = ttk.Frame(main_interaction_frame)

input_frame = tk.Frame(main_interaction_frame)


# Создаем рамку для содержания команды записи m и b
entry_b_m_frame = tk.Frame(input_frame)


# Создаем рамку для цикла записи скорости под разными углами (0,5,10,15)
velocity_angle_loop_frame = tk.Frame(input_frame)


# Создаем рамку для записи определенного угла и скорости
velocity_angle_const_frame = tk.Frame(input_frame)


# Создаем рамку для записи опорных сигналов
oporn_signal_frame = tk.Frame(input_frame)

# Создаем рамку для отключения тока удержания
cur_off_frame = tk.Frame(input_frame)

#################################


# Создаем метку для надписи над окном вывода
comport_title_label = tk.Label(comport_frame)

# Создаем метку для надписи над окном вывода
parameters_title_label = tk.Label(parameters_frame)

# Создаем метку для надписи над окном вывода
# entry_b_m_title_label = tk.Label(entry_b_m_frame)


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
#values = serial_ports()
combo1 = ttk.Combobox(comport_frame, width=22)
combo1.bind('<Button-1>', fill_combobox)

combo1.set("Выберите COMport №1")

# Создание Combobox
#values = serial_ports()
combo2 = ttk.Combobox(comport_frame, width=22)
combo2.bind('<Button-1>', fill_combobox)

combo2.set("Выберите COMport №2")

status = tk.StringVar(comport_frame)
status_label = tk.Label(comport_frame, textvariable=status)
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


# tooltip_label = ttk.Label(comport_frame, background="#ffffe0", relief="solid", borderwidth=1, wraplength=150)
# #tooltip_label.pack(ipadx=2, ipady=2, padx=10, pady=5)
# tooltip_label.config(font=("Helvetica", "8"))
# create_tooltip(output_m_b_text, "Отображение параметра b")

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


# tooltip_label = ttk.Label(root, background="#ffffe0", relief="solid", borderwidth=1, wraplength=150)
# #tooltip_label.pack(ipadx=2, ipady=2, padx=10, pady=5)
# tooltip_label.config(font=("Helvetica", "8"))
# create_tooltip(output_c1_c2_text, "Отображение параметров с1, с2")


##################################

# Кнопка для команды на запись опорных сигналов
oporn_signal_button = Mutton(oporn_signal_frame, text="Запись опорных сигналов", command=write_oporn_sign)


# Создание окна для оповещения о завершении процесса записи опорных векторов
end_write_oporn_var = tk.StringVar(oporn_signal_frame, f"здесь будет оповещение о завершении записи")
end_write_oporn = tk.Label(oporn_signal_frame, textvariable=end_write_oporn_var)

##################################

# Кнопка для оставновки тока удержания 
cur_off_button = Mutton(cur_off_frame, text="Отключение тока удержания", command=cur_off)

# Создание окна для оповещения о завершении процесса записи опорных векторов
end_write_curr_off_var = tk.StringVar(cur_off_frame, f"здесь будет оповещение об отключении тока")
cur_off_info = tk.Label(cur_off_frame, textvariable=end_write_curr_off_var)

##################################

# Слева колонка для отображения портов, прошивки и некоторых статусов


def build_app():
    comport_frame.grid(row=0, column=0, rowspan=4, padx=(10, 10))
    com_port_frame_separator.grid(row=0, column=1, sticky="ewns")
    main_interaction_frame.grid(row=0, column=2)
    build_comport_frame()
    build_main_interaction_frame()
    build_parameters_frame()
    build_input_frame()


def build_comport_frame():
    """
    Установка виджетов связанных с СОМ портами
    """
    combo1.grid(row=0, column=0, pady=5)
    combo2.grid(row=1, column=0, pady=5)
    button_open_port.grid(row=2, column=0, pady=(10,5))
    button_close_port.grid(row=3, column=0)
    info_vers_label.grid(row=4, column=0, padx=0, pady=15)
    status_label.grid(row=5, column=0, sticky="sew")
    


def build_main_interaction_frame():
    """Основной фрэйм для взаимодействия пользователя
    """
    input_frame.grid(row=0, column=0, sticky="w")
    parameters_frame.grid(row=1, column=0, pady=10)


def build_parameters_frame():
    """Фрэйм для отображения текущих параметров
    """
    parameters_vel_text.grid(
        row=0, column=0, padx=0, pady=0)
    vel_label.grid(
        row=1, column=0, pady=(5,25))
    
    parameters_angle_text.grid(
        row=0, column=1, padx=0, pady=0)
    angle_label.grid(
        row=1, column=1, pady=(5,25))

    parameters_m12_text.grid(
        row=0, column=2, padx=15, pady=0)
    m12_label.grid(
        row=1, column=2, pady=(5,25))
    
    parameters_m21_text.grid(
        row=0, column=3, padx=15, pady=0)
    m21_label.grid(
        row=1, column=3, pady=(5,25))
    
    parameters_m34_text.grid(
        row=0, column=4, padx=0, pady=0)
    m34_label.grid(
        row=1, column=4, pady=(5,25))
    
    parameters_m43_text.grid(
        row=2, column=0, padx=0, pady=0)
    m43_label.grid(
        row=3, column=0, pady=(5,25))
    
    parameters_t1_text.grid(
        row=2, column=1, padx=0, pady=0)
    t1_label.grid(
        row=3, column=1, pady=(5,25))
    
    parameters_t2_text.grid(
        row=2, column=2, padx=0, pady=0)
    t2_label.grid(
        row=3, column=2, pady=(5,25))
    
    parameters_t3_text.grid(
        row=2, column=3, padx=0, pady=0)
    t3_label.grid(
        row=3, column=3, pady=(5,25))
    parameters_t4_text.grid(
        row=2, column=4, padx=0, pady=0)
    t4_label.grid(
        row=3, column=4, pady=(5,25))


def build_input_frame():
    entry_b_m_frame.grid(row=0, column=0, padx=10, pady=0, sticky="w")
    velocity_angle_loop_frame.grid(row=1, column=0, padx=10, pady=0, sticky="w")
    velocity_angle_const_frame.grid(row=2, column=0, padx=10, pady=0, sticky="w")
    oporn_signal_frame.grid(row=3, column=0, padx=10, pady=0, sticky="w")
    cur_off_frame.grid(row=4, column=0, padx=10, pady=0, sticky="w")

    build_input_minor_frames()


def build_input_minor_frames():
    input_m_b_button.grid(row=0, column=0, padx=10, pady=1)
    entry_m_b.grid(row=0, column=1)
    output_m_b_text.grid(row=0, column=2, padx=20, pady=1) 

    velocity_angle_loop_button.grid(row=0, column=0, padx=10, pady=1)
    entry_velocity_angle.grid(row=0, column=1)
    velocity_angle_loop_info.grid(row=0, column=2)

    velocity_angle_const_button.grid(row=0, column=0, padx=10, pady=1)
    entry_velocity_const.grid(row=0, column=1)
    entry_angle_const.grid(row=0, column=2, padx=20, pady=1)
    output_c1_c2_text.grid(row=0, column=3, padx=0, pady=1)
    oporn_signal_button.grid(row=0, column=0, padx=10, pady=1)
    end_write_oporn.grid(row=0, column=1, padx=10, pady=1)
    cur_off_button.grid(row=0, column=1, padx=10, pady=10)  
    cur_off_info.grid(row=0, column=2, padx=10, pady=10)


build_app()


# Основной фрэйм












NAME_PARAM = [parameters_vel_text,
              parameters_angle_text,
              parameters_m12_text,
              parameters_m21_text,
              parameters_m34_text,
              parameters_m43_text,
              parameters_t1_text,
              parameters_t2_text,
              parameters_t3_text,
              parameters_t4_text]
ALL_BUTTONS = [button_open_port,button_close_port,
               input_m_b_button,velocity_angle_loop_button,
               velocity_angle_const_button,oporn_signal_button,
               cur_off_button]
root.mainloop()