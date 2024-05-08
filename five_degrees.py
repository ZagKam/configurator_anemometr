import serial 
import struct
import time

from serialport import Serial
from program_logger import logger


READ_TIMEOUT = 40
def rotation_five_degree(ComPort: Serial) -> bool:
    """
    Функция для записи опорных сигналов.
        
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
    Возвращает: 
        - bool: когда приходит ответ, функция вернет True
        
        ПРМЕЧАНИЕ: Эта функция с шаговым двигателем
    """
    byte_request = b'\x01\x06\x00\x1C\x00\x01\x89\xCC' 
    
    try: 
        answer = list(ComPort.interact(byte_request, read_size=8, read_timeout=READ_TIMEOUT))
        time.sleep(0.25)
    except Exception as e:
        logger.error(e)
        return False
    logger.debug(f"Motor has rotated {answer=}")
    return True


def initial_calibration(port: Serial):
    """Make initial calibration for motor
    """
    byte_request = b'\x01\x10\x00\x1A\x00\x02\x04\x00\xB2\x00\x00\xD2\xFB' 
    answer = port.interact(byte_request, read_size=8)
    logger.debug(f"For motor intial step was set {answer=}")