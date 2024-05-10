from velocity_direct_wind import wind_vel_direct
from calibr_koef import calibration_koef
from data_logger import add_line
from serialport import Serial
from five_degrees import rotation_five_degree

from config import config


def calibration_loop(ui_update: callable, wind_velocity: int, port_uz: Serial,
                     port_js: Serial):
    
    
    for i in range(config["calibration_step_number"] + 1):
        angle = round(i * (360 / config["calibration_step_number"]))
        wind_vel_direct(port_uz, str(wind_velocity),
                        str(angle))
        # Наиль, команда wind_vel_direct обрабатывается около 30 секунд, 
        # там нужно ждать ответа и потом уже использовать следующую команду 
        # в логгер записывать только c1, c2, логгер вроде как сделал, но хз 
        # как работает
        c1, c2 = calibration_koef(port_uz,
                                  wind_velocity,
                                  angle) #
        
        add_line(c1, c2)
        # также здесь должен быть вывод угла на экран конфигуратора, угл и скорость
        ui_update(wind_velocity, angle, c1, c2)
        rotation_five_degree(port_js)
