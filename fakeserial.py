from unittest.mock import Mock
from time import sleep

class TestSerial(Mock):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.command = b''
    
    def read(self, *args, **kwargs):
        sleep(0.15)
        match self.command:
            case b'\x3C\x03\x00\x01\x00\x02\x91\x26': 
                return b'\x3C\x03\x04\x00\x00\x00\x0A\x96\xF7'
        
    def write(self, command: bytes,  *args, **kwargs):
        self.command = command


if __name__ == '__main__':
    ser = TestSerial()
    print(ser.read(b'\x3C\x03\x00\x01\x00\x02\x91\x26'))