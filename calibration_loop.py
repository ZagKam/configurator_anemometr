from velocity_direct_wind import wind_vel_direct
from calibr_koef import calibration_koef
from data_logger import add_line


def zaloopa():
    for i in range(71):
        #
        wind_vel_direct
        # Наиль, команда wind_vel_direct обрабатывается около 30 секунд, 
        # там нужно ждать ответа и потом уже использовать следующую команду 
        # в логгер записывать только c1, c2, логгер вроде как сделал, но хз 
        # как работает
        c1, c2 = calibration_koef #
        
        add_line(c1, c2)
        # также здесь должен быть вывод угла на экран конфигуратора, угл и скорость