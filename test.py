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
import tkinter as tk

def display_text():
    text = entry.get()
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)
    output_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Пример поля вывода")

entry = tk.Entry(root)
entry.grid(row=0, column=0, padx=10, pady=10)

display_button = tk.Button(root, text="Показать текст", command=display_text)
display_button.grid(row=0, column=1, padx=10, pady=10)

output_text = tk.Text(root, height=10, width=40)
output_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

