import serial 
import struct
from build_request import build_request

def calibration_koef(ComPort:serial.Serial, velocity:str, angle:str) -> list[float, float]:
    
    """
    Функция для установки параметра sens для выбранного газа.
    
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
        - velocity: str строковое значение вводимого параметра вида int. 
        - angle: str строковое значение вводимого параметра вида int. 
        
        Возвращает: 
        - list[float16, float16]: list, где внутри находится 2 значения float.

    """
    
    scaled_velocity = int(velocity)
    scaled_angle = int(int(angle) / 5)
    hex_velocity = format(scaled_velocity, '02X')
    hex_angle = format(scaled_angle, '02X')
    request = '3C04' + hex_velocity + hex_angle + '0002'
    byte_request = build_request(request)
    try:
        raw_answer = ComPort.interact(byte_request, read_size=9)
        if raw_answer == []:
            return '-1'
    except Exception as e:
        print(e) 
        
    
    # ##### не проверена работоспособность кода преобразующего u16 в halffloat
    half_float_c1 = struct.unpack('<e', raw_answer[3:5])[0]
    half_float_c2 = struct.unpack('<e', raw_answer[5:7])[0]
    # ####
    
    list_answer = [round(half_float_c1, 3), round(half_float_c2, 3)]
    
    return list_answer

# if __name__ == "__main__":
#     import serial 
#     import struct
#     from build_request import build_request


#     ComPort = serial.Serial('COM4', timeout=1) 
#     ComPort.baudrate = 19200 
#     ComPort.bytesize = 8    
#     ComPort.parity = 'N'  
#     ComPort.stopbits = 1  
#     ComPort.write(b'\x3C\x04\x00\x00\x00\x02\x75\x26' )
#     raw_answer = list(ComPort.read(9))
#     print(raw_answer)
