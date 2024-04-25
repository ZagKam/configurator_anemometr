import serial 
from build_request import build_request


def set_m(ComPort:serial.Serial, value_m:str) -> int:
    """
    Функция для установки параметра m для выбранного газа.
    
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
        - value_m: str строковое значение вводимого параметра вида int. 
    Возвращает:
        - b_value: int число преобразованное
    """
    scaled_value = int(value_m)
    hex_value = format(scaled_value, '04X')
    request = '3C060001' + hex_value
    byte_request = build_request(request)
    try:
        ComPort.write(byte_request)
        raw_answer = list(ComPort.read(9))
        if raw_answer == []:
            return '-1'
    except Exception as e:
        print(e) 
    hex_answer = ''
    for number in raw_answer[5:7]:
        hex_answer += format(number, '02X')
    return int(hex_answer, 16)
    
    