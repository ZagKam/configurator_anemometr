import serial 
import struct
import time

def entry_oporn_signal(ComPort:serial.Serial) -> bool:
    """
    Функция для записи опорных сигналов.
        
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
    Возвращает: 
        - bool: когда приходит ответ, функция вернет True.
    """
    byte_request = b'\x3C\x06\x00\x00\x00\x00\x8D\x27' 
    
    while len(answer) == 0:
        try: 
            answer = list(ComPort.interact(byte_request, read_size=8))
            time.sleep(0.25)
        except Exception as e:
            print(e)
    return True
    
    