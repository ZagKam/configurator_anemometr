import serial 
import struct
from date_time import time_now
import os


def log_read(ComPort:serial.Serial) -> None:
    """
    Функция для записи значений в файл (m12, m21, m34, m43, t1, t2, t3, t4).
        
    Аргументы:
        - ComPort: seiralSerial класс бибилеотки serial для подключения к плате;
    Возвращает: 
    """
    device_name = 'Logger'
    
    ser = ComPort
    
    TIMEOUT = 1
    while True:
        time = time_now()
        write_path = device_name + '.csv'
        mode = 'a' if os.path.exists(write_path) else 'w'    

        with open(write_path, mode) as file:
            try:
                ser.write(b'\x3C\x03\x00\x00\x00\x0A\xC1\x20') 
                velocity_speed_wind = ser.read(25)
                time.sleep(0.05)        
                
                print((velocity_speed_wind))

                if len(velocity_speed_wind) != 25:
                    raise ValueError("Incomplete response received.")
                
                velocity_speed_wind_data = [(struct.unpack(">H", velocity_speed_wind[3:5][0]))/10, 
                                            struct.unpack(">H", velocity_speed_wind[5:7][0]), 
                                            struct.unpack(">H", velocity_speed_wind[7:9][0]), 
                                            struct.unpack(">H", velocity_speed_wind[9:11][0]), 
                                            struct.unpack(">H", velocity_speed_wind[11:13][0]), 
                                            struct.unpack(">H", velocity_speed_wind[13:15][0]), 
                                            struct.unpack(">H", velocity_speed_wind[15:17][0]), 
                                            struct.unpack(">H", velocity_speed_wind[17:19][0]),
                                            struct.unpack(">H", velocity_speed_wind[19:21][0]),
                                            struct.unpack(">H", velocity_speed_wind[21:23][0])]  
                
                
                line = ','.join(map(str, velocity_speed_wind_data)) + '\n'
                time.sleep(TIMEOUT)  
                
                if mode == 'w':  
                    file.write('Date, wind_velocity, wind_direction, m_12, m_21, m_34, m43, t1, t2, t3, t4, \n')

                file.write(time_now + ',' + line)
                
            except Exception as e:
                print(e)
                time.sleep(TIMEOUT)