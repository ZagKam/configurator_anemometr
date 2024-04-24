import crcmod


def get_crc(hex_string:str) -> str:
    """
    Функция подсчета контрольной суммы hex-строки.
    
    Аргументы:
        - hex_string: str строка с hex-значением. Пример: 2A40
    
    Возвращает:
        - hex_string_crc: str строка с hex-значением.
    """
    byte_string = bytes.fromhex(hex_string)
    crc16 = crcmod.mkCrcFun(0x18005, initCrc=0xFFFF, rev=True,  xorOut=0x0000)
    crc_int = crc16(byte_string)
    
    crc_str = format(crc_int, '06X')[2:]

    hex_string_crc = crc_str[2:5] + crc_str[0:2] 
    return hex_string_crc
    
    
    
