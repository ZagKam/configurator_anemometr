import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from serial_ports import serial_ports
import serial
from get_version import get_version
from fakeserial import read()


class Mutton(ttk.Button):
    ...


def show_message():
    messagebox.showinfo("Сообщение", "Вы нажали кнопку!")

def get_input():
    input_text = entry.get()
    messagebox.showinfo("Поле ввода", f"Вы ввели: {input_text}")

def check_state():
    if var.get() == 1:
        messagebox.showinfo("Чекбокс", "Чекбокс отмечен")
    else:
        messagebox.showinfo("Чекбокс", "Чекбокс не отмечен")

# Создание главного окна
root = tk.Tk()
root.title("Пример GUI")

# Установка размеров окна
root.geometry("900x300")  # Ширина x Высота

# Создание Combobox
values = serial_ports()
combo1 = ttk.Combobox(root, values=values, width=22)
combo1.grid(row=0, column=0, padx=10, pady=10)
combo1.set("Выберите COMport №1")

# Создание Combobox
values = serial_ports()
combo2 = ttk.Combobox(root, values=values, width=22)
combo2.grid(row=0, column=1, padx=10, pady=10)
combo2.set("Выберите COMport №2")

# Создание кнопки и размещение с помощью grid
button_open_port = Mutton(root, text="Открыть порты", command=show_message)
button_open_port.grid(row=0, column=2, padx=10, pady=10)


# Создание кнопки и размещение с помощью grid
button_close_port = Mutton(root, text="Закрыть порты", command=show_message)
button_close_port.grid(row=0, column=3, padx=10, pady=10)


# Создаем рамку для содержания метки и окна вывода
output_frame = tk.Frame(root)
output_frame.grid(row=0, column=3, padx=10, pady=5, sticky='n')

# Создаем метку для надписи над окном вывода
output_title_label = tk.Label(output_frame, text="Версия:")
output_title_label.grid(row=0, column=0, padx=10, pady=(0, 5))

# Создание окна вывода, для вывода версии
output_text = tk.Text(output_frame, width=15, height=1)
output_text.grid(row=1, column=0, padx=10, pady=(0, 10))
output_text.insert(tk.END, get_version())




# Создание кнопки и размещение с помощью grid
button = tk.Button(root, text="Нажми меня", command=show_message)
button.grid(row=5, column=0, padx=10, pady=10)

# Создание поля ввода и размещение с помощью grid
entry = tk.Entry(root)
entry.grid(row=1, column=0, padx=10, pady=10)

# Создание кнопки для получения данных из поля ввода и размещение с помощью grid
input_button = tk.Button(root, text="Получить данные", command=get_input)
input_button.grid(row=2, column=0, padx=10, pady=10)

# Создание чекбокса и размещение с помощью grid
var = tk.IntVar()
checkbox = tk.Checkbutton(root, text="Отметить", variable=var, command=check_state)
checkbox.grid(row=3, column=0, padx=10, pady=10)

# Создание Combobox
values = ["Вариант 1", "Вариант 2", "Вариант 3"]
combo = ttk.Combobox(root, values=values)
combo.grid(row=4, column=0, padx=10, pady=10)
combo.set("Выберите вариант")

# Запуск главного цикла обработки событий
root.mainloop()