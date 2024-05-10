import serial 
import struct
import time

from config import config
from get_crc import get_crc

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
    byte_request = config["current_off_command"]
    
    try: 
        answer = list(ComPort.interact(byte_request, read_size=config["current_off_answer_size"], read_timeout=READ_TIMEOUT))
        time.sleep(0.25)
    except Exception as e:
        print(e)
        return False
    return True