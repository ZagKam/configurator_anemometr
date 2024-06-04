import serial 
import struct
import time

from serialport import Serial
from program_logger import logger
from config import config


READ_TIMEOUT = config["motor_rotation_duration"]
def rotation_five_degree(ComPort: Serial) -> bool:
    """
    Функция для записи опорных сигналов.
        
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
    Возвращает: 
        - bool: когда приходит ответ, функция вернет True
        
        ПРМЕЧАНИЕ: Эта функция с шаговым двигателем
    """
    byte_request = config['motor_rotation_commmand']
    
    try: 
        answer = list(ComPort.interact(byte_request, 
                                       read_size=config["motor_rotation_answer_size"], 
                                       read_timeout=READ_TIMEOUT))
        time.sleep(0.25)
    except Exception as e:
        logger.error(e)
        return False
    logger.debug(f"Motor has rotated {answer=}")
    return True
    # "motor_position": "0103001E0002A40D", - команда для обнаружения позиции

def initial_calibration(port: Serial):
    """Make initial calibration for motor
    """
    byte_request = config["motor_configuration_command"]
    answer = port.interact(byte_request, read_size=config["motor_configuration_answer_size"])
    logger.debug(f"For motor intial step was set {answer=}")