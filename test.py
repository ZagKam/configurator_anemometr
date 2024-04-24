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
# velocity_speed_wind = b'\x3C\x03\x00\x00\x00\x0A\xC1\x20'
# print((struct.unpack(">H", velocity_speed_wind[1:3])[0]))

hex_answer = '03FF'
print(int(hex_answer, 16))