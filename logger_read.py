import serial
import datetime
import os
import time

ser_port = 'COM4'

device_name = 'Logger'

ser = serial.Serial(ser_port, baudrate=19200, bytesize=8, stopbits=1, timeout=1)
print(ser)
logger_path = device_name

TIMEOUT = 1
while True:
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_path = logger_path + '.csv'

    mode = 'a' if os.path.exists(write_path) else 'w'

    with open(write_path, mode) as file:  # Use write_path instead of 'Logger.csv'
        try:
            ser.write(b'\x3C\x03\x00\x00\x00\x02\xC0\xE6') 
            velocity_wind = ser.read(9)
            time.sleep(0.05)
            ser.write(b'\x3C\x06\x00\x00\x00\x00\x8D\x27') 
            reference_signals = ser.read(8)
            time.sleep(0.05)
            ser.write(b'\x3D\x03\x00\x00\x00\x02\xC1\x37')
            max_m12_m21 = ser.read(9)
            time.sleep(0.05)
            ser.write(b'\x3E\x03\x00\x00\x00\x02\xC1\x04')
            max_m34_m43 = ser.read(9)
            time.sleep(0.05)
            ser.write(b'\x3C\x03\x00\x01\x00\x02\x91\x26') 
            vers_firmware = ser.read(9)
            time.sleep(0.05)
            
            ser.write(b'\x3C\x03\x00\x00\x00\x0A\xC1\x20') 
            vers_firmware = ser.read(9)
            time.sleep(0.05)
            
            
            print((velocity_wind))
            print((reference_signals))
            print((max_m12_m21))
            print((max_m34_m43))
            print((vers_firmware))
            if len(velocity_wind) != 9 or len(max_m12_m21) != 9 or len(max_m34_m43) != 9:
                raise ValueError("Incomplete response received.")

            velocity_wind_data = [(velocity_wind[3]*256 + velocity_wind[4])/10, velocity_wind[5]*256 + velocity_wind[6]]
            max_m12_m21_data = [max_m12_m21[3]*256 + max_m12_m21[4], max_m12_m21[5]*256 + max_m12_m21[6]]
            max_m34_m43_data = [max_m34_m43[3]*256 + max_m34_m43[4], max_m34_m43[5]*256 + max_m34_m43[6]]

            line = ','.join(map(str, velocity_wind_data)) + ',' + ','.join(map(str, max_m12_m21_data)) + ',' + ','.join(map(str, max_m34_m43_data)) + ',' + '\n'
            time.sleep(TIMEOUT)  
            
            if mode == 'w':  # Only write header if the file is newly created
                file.write('Date, wind_velocity, wind_direction, m_12, m_21, m_34, m43\n')

            file.write(time_now + ',' + line)
            
        except Exception as e:
            print(e)
            time.sleep(TIMEOUT)