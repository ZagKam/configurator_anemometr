import serial 
import struct
from date_time import time_now
import os
import time


def all_params(ComPort:serial.Serial) -> None:
    """
    Функция для вывода значений  (m12, m21, m34, m43, t1, t2, t3, t4).
        
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
    Возвращает: 
    """
    device_name = 'Logger'
    
    ser = ComPort
    
    TIMEOUT = 1
    while True:
        try:
            ser.write(b'\x3C\x03\x00\x00\x00\x0A\xC1\x20') 
            velocity_speed_wind = ser.read(25)
            time.sleep(0.05)        
            
            print((velocity_speed_wind))

            if len(velocity_speed_wind) != 25:
                raise ValueError("Incomplete response received.")
            
            parameters_data = [(struct.unpack(">H", velocity_speed_wind[3:5]))[0]/10, 
                                        struct.unpack(">H", velocity_speed_wind[5:7])[0], 
                                        struct.unpack(">H", velocity_speed_wind[7:9])[0], 
                                        struct.unpack(">H", velocity_speed_wind[9:11])[0], 
                                        struct.unpack(">H", velocity_speed_wind[11:13])[0], 
                                        struct.unpack(">H", velocity_speed_wind[13:15])[0], 
                                        struct.unpack(">H", velocity_speed_wind[15:17])[0], 
                                        struct.unpack(">H", velocity_speed_wind[17:19])[0],
                                        struct.unpack(">H", velocity_speed_wind[19:21])[0],
                                        struct.unpack(">H", velocity_speed_wind[21:23])[0]] 
            
            return parameters_data
        except Exception as e:
            print("On all_params", e)
            time.sleep(TIMEOUT)