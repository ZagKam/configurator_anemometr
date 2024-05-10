import serial 
import struct
import time

from config import config

READ_TIMEOUT = config["oporn_signal_set_duration"]
def entry_oporn_signal(ComPort:serial.Serial) -> bool:
    """
    Функция для записи опорных сигналов.
        
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
    Возвращает: 
        - bool: когда приходит ответ, функция вернет True.
    """
    byte_request = config["oporn_signal_set_command"] 

    try: 
        answer = list(ComPort.interact(byte_request, 
                                       read_size=config["oporn_signal_set_answer_size"], 
                                       read_timeout=READ_TIMEOUT))
        time.sleep(0.25)
    except Exception as e:
        print(e)
    return True
    
    