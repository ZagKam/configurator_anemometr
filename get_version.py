import serial 
import struct
import time

from config import config


def get_version(ComPort:serial.Serial) -> int:
    """
    Функция для получения версии анемометра.
        
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
    Возвращает: 
        - str версию газоанализатора.
    """
    byte_request = config["get_version_command"]
    answer = list(ComPort.interact(byte_request, read_size=9))
    time.sleep(0.25) 
    try:
        if not answer:
            print('No answer on', ComPort)
            return -1
        if answer[5] == 0:
            return answer[6]
        else:
            two_byte = answer[5].to_bytes(1, 'big') + answer[6].to_bytes(1, 'big')
            concat_byte = list(struct.unpack('>H', two_byte))
            return concat_byte
    except Exception as e:
        print(e)
        return -1
        #ComPort.close()
       
    
    
if __name__ == "__main__":
    from serialport import Serial
    ComPort = Serial('COM4', timeout=1)
    ComPort.baudrate = 19200
    ComPort.bytesize = 8
    ComPort.parity = 'N'
    ComPort.stopbits = 1
    print(get_version(ComPort))