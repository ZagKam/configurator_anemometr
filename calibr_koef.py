import serial 
import struct
from build_request import build_request

def calibration_koef(ComPort:serial.Serial, velocity:str, angle:str) -> list[int, int]:
    
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
    scaled_angle = int(angle) / 5
    hex_velocity = format(scaled_velocity, '04X')
    hex_angle = format(scaled_angle, '04X')
    request = '3C04' + hex_velocity + hex_angle + '0002'
    byte_request = build_request(request)
    try:
        ComPort.write(byte_request)
        raw_answer = list(ComPort.read(9))
        if raw_answer == []:
            return '-1'
    except Exception as e:
        print(e) 
    hex_c1 = ''
    for number in raw_answer[4:6]:
        hex_c1 += format(number, '02X')
        
    hex_c2 = ''    
    for number in raw_answer[4:6]:
        hex_c2 += format(number, '02X')
        
    
    ##### не проверена работоспособность кода преобразующего u16 в halffloat
    half_float_c1 = struct.unpack('<e', struct.pack('<H', hex_c1))[0]
    half_float_c2 = struct.unpack('<e', struct.pack('<H', hex_c2))[0]
    ####
    
    list_answer = [half_float_c1, half_float_c2]
    
    return list_answer






