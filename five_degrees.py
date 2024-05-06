import serial 
import struct
import time

def rotation_five_degree(ComPort:serial.Serial) -> bool:
    """
    Функция для записи опорных сигналов.
        
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
    Возвращает: 
        - bool: когда приходит ответ, функция вернет True
        
        ПРМЕЧАНИЕ: Эта функция с шаговым двигателем
    """
    byte_request = b'\x01\x10\x00\x1A\x00\x02\x04\x00\xB2\x00\x00\xD2\xFB' 
    
    while len(answer) == 0:
        try: 
            answer = list(ComPort.interact(byte_request, read_size=8))
            time.sleep(0.25)
        except Exception as e:
            print(e)
    return True