from serialport import Serial 
import struct
from build_request import build_request


def wind_vel_direct(ComPort:Serial, velocity:str, angle:str) -> int:
    
    """
    Функция для установки параметра sens для выбранного газа.
    
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
        - velocity: str строковое значение вводимого параметра вида int. 
        - angle: str строковое значение вводимого параметра вида int. 
        
        Возвращает: 
        - number_reg: int значение.

    """
    request_process_duration = 40
    scaled_velocity = int(velocity)
    scaled_angle = int(angle)
    hex_velocity = format(scaled_velocity, '04X')
    hex_angle = format(scaled_angle, '04X')
    request = '3C100002000204' + hex_velocity + hex_angle
    byte_request = build_request(request)
    try:
        raw_answer = list(ComPort.interact(byte_request, read_size=8, read_timeout=request_process_duration))
        if raw_answer == []:
            return '-1'
    except Exception as e:
        print(e) 
    hex_answer = ''
    for number in raw_answer[4:6]:
        hex_answer += format(number, '02X')
    return int(hex_answer, 16)
    
    
    