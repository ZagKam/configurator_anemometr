from unittest.mock import Mock
from threading import Lock, RLock, current_thread
from time import sleep
import serial
import os
from time import sleep
from random import random
from config import config
from program_logger import logger


class SerialMock(Mock):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.command = b''
        self.closed = False

    def close(self):
        self.closed = True
        
    
    def read(self, command:bytes, *args, **kwargs):
        sleep(0.15)
        if command == b'\x3C\x03\x00\x01\x00\x02\x91\x26': 
                return b'\x3C\x03\x04\x00\x00\x00\x0A\x96\xF7'
        
    def write(self, command: bytes,  *args, **kwargs):
        self.command = command

    def interact(self, *args, read_size, read_timeout=0, **kwargs):
        if self.closed:
            raise ConnectionError()
        if read_timeout:
            sleep(read_timeout)
        return  bytearray([round(random() * 255) for _ in range(read_size)])


if config["test"]:

    class Serial(Mock):
        
        def __init__(self, *args, **kwargs):
            super().__init__()
            self.command = b''
            self.closed = False

        def close(self):
            self.closed = True
            
        
        def read(self, command:bytes, *args, **kwargs):
            sleep(0.15)
            if command == b'\x3C\x03\x00\x01\x00\x02\x91\x26': 
                    return b'\x3C\x03\x04\x00\x00\x00\x0A\x96\xF7'
            
        def write(self, command: bytes,  *args, **kwargs):
            self.command = command

        def interact(self, *args, read_size, read_timeout=0, **kwargs):
            if self.closed:
                raise ConnectionError()
            if read_timeout:
                sleep(read_timeout)
            return  bytearray([round(random() * 255) for _ in range(read_size)])
else:

    class Serial(serial.Serial):
        
        mutex = Lock()
        _is_calibration = False

        def enter_calibration(self):
            self._is_calibration = True
        
        def exit_calibration(self):
            self._is_calibration = False

        def write(self):
            raise PermissionError("The method is private. Use interact instead")
        
        def read(self):
            raise PermissionError("The method is private. Use interact instead")
        
        def interact(self, *args, read_size=0,
                    read_timeout=0.4, **kwargs) -> bytes:
            """During calibration only CalibrationThread named thread can 
            interact with the port

            :param read_size: _description_, defaults to 0
            :type read_size: int, optional
            :param read_timeout: _description_, defaults to 1
            :type read_timeout: int, optional
            :return: _description_
            :rtype: _type_
            """
            with self.mutex:
                if self._is_calibration and current_thread().name != "CalibrationThread":
                    return b"" 
                inwaiting = self.in_waiting
                if inwaiting:
                    logger.debug(f"{inwaiting=}")
                    print(f"Unxpected bytes on port {self.read(inwaiting)}")
                super().write(*args, **kwargs)
                sleep(0.05)
                if self.timeout != read_timeout:
                    self.timeout = read_timeout
                if read_size:
                    ans = super().read(read_size)
                else:
                    ans =  super().read_all()
                sleep(0.05)
                return ans

#from serial import Serial

if __name__ == '__main__':
    ser = Serial()
    ser.open()
    ser.open("motherfucker")
    ser.fungorn.close()
    print(ser.read(b'\x3C\x03\x00\x01\x00\x02\x91\x26'))
    
