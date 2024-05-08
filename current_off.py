import serial 
import struct
import time

READ_TIMEOUT = 40
def current_off(ComPort:serial.Serial) -> bool:
    """
    Функция для отключения тока.
        
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
    Возвращает:
        - bool: когда приходит ответ, функция вернет True
        
        ПРМЕЧАНИЕ: Эта функция с шаговым двигателем
    """
    byte_request = b'\x01\x10\x00\x0E\x00\x01\x02\x00\x00\xA7\x7E' 
    
    try: 
        answer = list(ComPort.interact(byte_request, read_size=8, read_timeout=READ_TIMEOUT))
        time.sleep(0.25)
    except Exception as e:
        print(e)
    return True