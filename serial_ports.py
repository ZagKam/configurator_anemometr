import serial
from typing import List
from serial import SerialException
from time import sleep

from program_logger import logger

def serial_ports() -> List[str]:
    """
    Функция определения COM-порт в windows
    
    Возвращает:
        -result:List[str]
    """
    ports = ['COM%s' % (i + 1) for i in range(256)]
    list_of_ports = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            sleep(0.05)
            list_of_ports.append(port)
            logger.debug(f"Found COM port {port}")
        except (OSError, serial.SerialException) as e:
            try:
                
                s = serial.Serial(port, 9600)
                s.close()
            except:
                pass
                try:
                    s = serial.Serial(port, 19200)
                    s.close()
                except:
                    pass
                
            pass
    if list_of_ports:
        logger.debug(f"Found COM port {list_of_ports}")
    return list_of_ports





if __name__ == "__main__":
    list_of_ports = serial_ports()
    print(list_of_ports)