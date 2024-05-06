from unittest.mock import Mock
from threading import Lock
from time import sleep
import serial

class Serial(Mock):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.command = b''
    
    def read(self, command:bytes, *args, **kwargs):
        sleep(0.15)
        match command:
            case b'\x3C\x03\x00\x01\x00\x02\x91\x26': 
                return b'\x3C\x03\x04\x00\x00\x00\x0A\x96\xF7'
        
    def write(self, command: bytes,  *args, **kwargs):
        self.command = command

class Serial(serial.Serial):
    
    mutex = Lock()
    
    def interact(self, *args, read_size=0, **kwargs):
        with self.mutex:
            super().write(*args, **kwargs)
            
            if read_size:
                return super().read(read_size)
            super().read_all()

#from serial import Serial

if __name__ == '__main__':
    ser = Serial()
    ser.open()
    ser.open("motherfucker")
    ser.fungorn.close()
    print(ser.read(b'\x3C\x03\x00\x01\x00\x02\x91\x26'))
    
