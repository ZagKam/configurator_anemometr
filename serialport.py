from unittest.mock import Mock
from time import sleep

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


#from serial import Serial

if __name__ == '__main__':
    ser = TestSerial()
    ser.open()
    ser.open("motherfucker")
    ser.fungorn.close()
    print(ser.read(b'\x3C\x03\x00\x01\x00\x02\x91\x26'))
    
