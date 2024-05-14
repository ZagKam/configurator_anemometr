# from unittest.mock import Mock

# class TestSerial(Mock):
    
#     def __init__(self, *args, **kwargs):
#         super().__init__()
#         self.command = b''
    
#     def read(self, *args, **kwargs):
#         match self.command:
#             case b'\x3C\x03\x00\x00\x00\x0A\xC1\x20': 
#                 return 
        
#     def write(self, command: bytes,  *args, **kwargs):
#         self.command = command












# ww = 255
# ee = 0
# print(ee.to_bytes(1, 'big') + ww.to_bytes(1, 'big'))


# def sum_byte(num1, num2):
#     # Преобразуем числа в байты в шестнадцатеричном формате
#     byte1 = bytes([num1])
#     byte2 = bytes([num2])

#     # Объединяем байты в один байт
#     combined_byte = byte1 + byte2

#     # Преобразуем объединенный байт в число
#     result = int.from_bytes(combined_byte, byteorder='big')
#     return(result)

# print(sum_byte(3, 255))
# import struct
# raw_answer = b'\x3C\x03\x00\x00\x00\x0A\xC1\x20'
# print((struct.unpack(">H", raw_answer[1:3])[0]))
# hex_answer = ''
# for number in raw_answer[1:3]:
#     hex_answer += format(number, '02X')
# print(int(hex_answer, 16))
# import tkinter as tk

# def display_text():
#     text = entry.get()
#     output_text.config(state=tk.NORMAL)
#     output_text.delete("1.0", tk.END)
#     output_text.insert(tk.END, text)
#     output_text.config(state=tk.DISABLED)

# root = tk.Tk()
# root.title("Пример поля вывода")

# entry = tk.Entry(root)
# entry.grid(row=0, column=0, padx=10, pady=10)

# display_button = tk.Button(root, text="Показать текст", command=display_text)
# display_button.grid(row=0, column=1, padx=10, pady=10)

# output_text = tk.Text(root, height=10, width=40)
# output_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# root.mainloop()

# import tkinter as tk
# from tkinter import ttk

# def create_tooltip(widget, text):
#     widget.bind("<Enter>", lambda event: show_tooltip(text))
#     widget.bind("<Leave>", lambda event: hide_tooltip())

# def show_tooltip(text):
#     tooltip_label.config(text=text)
#     tooltip_label.place(relx=0.5, rely=0.5, anchor="center")

# def hide_tooltip():
#     tooltip_label.place_forget()

# root = tk.Tk()

# entry_b_m_frame = tk.Frame(root)
# entry_b_m_frame.pack()

# output_m_b_text = tk.Text(entry_b_m_frame)
# output_m_b_text.configure(width=15, height=1)
# output_m_b_text.grid(row=1, column=2, padx=20, pady=1)

# tooltip_label = ttk.Label(root, background="#ffffe0", relief="solid", borderwidth=1, wraplength=150)
# tooltip_label.pack(ipadx=2, ipady=2, padx=10, pady=5)
# tooltip_label.config(font=("Helvetica", "8"))

# create_tooltip(output_m_b_text, "Это поле вывода с подсказкой")

# root.mainloop()

# import time
# import serial

# try:
#     ComPort = serial.Serial('COM4', baudrate=19200)
#     print("Успешно открыт COM порт")

#     while True:
#         byte_request = b'\x3C\x03\x00\x01\x00\x02\x91\x26' 
#         ComPort.write(byte_request)
#         answer = list(ComPort.read(9))
#         print("Получен ответ:", answer)
#         time.sleep(1) 

# except KeyboardInterrupt:
#     # Закрываем COM порт при прерывании программы
#     ComPort.close()
#     print("Программа завершена")

# import tkinter as tk

# root = tk.Tk()
# root.title("Пример")

# parameters_frame = tk.Frame(root)
# parameters_frame.pack()

# label = tk.Label(parameters_frame, text="Метка:")
# label.pack()

# parameters_m12_text = tk.Text(parameters_frame)
# parameters_m12_text.configure(width=15, height=1)
# parameters_m12_text.pack()

# root.mainloop()
# scaled_velocity = 0
# print(format(scaled_velocity, '02X'))

# import tkinter as tk

# def button_clicked():
#     print("Button clicked")

# root = tk.Tk()
# root.geometry("200x200")
# root.configure(background='white')  # Установка фона

# # Создание кнопки
# invisible_button = tk.Button(root, text="Invisible Button", command=button_clicked, bg='white', bd=0, highlightthickness=0)
# invisible_button.place(x=50, y=50)

# root.mainloop()
import sys
print(sys.version)