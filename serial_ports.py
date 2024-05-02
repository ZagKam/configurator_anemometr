import serial
from typing import List
from serial import SerialException

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
            list_of_ports.append(port)
        except (OSError, serial.SerialException):
            pass
    return list_of_ports





if __name__ == "__main__":
    list_of_ports = serial_ports()
    print(list_of_ports)