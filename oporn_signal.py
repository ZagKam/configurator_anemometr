import serial 
import struct
import time

def entry_oporn_signal(ComPort:serial.Serial) -> int:
    """
    Функция для записи опорных сигналов.
        
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
    Возвращает: 
        - bytes байтовую строку (отправляется только после окончания записи).
    """
    byte_request = b'\x3C\x06\x00\x00\x00\x00\x8D\x27' 
    ComPort.write(byte_request) 
    answer = list(ComPort.read(11))
    
    while len(answer) == 0:
        try: 
            answer = list(ComPort.read(11))
            time.sleep(0.25)
        except Exception as e:
            print(e)
    return True
    
    