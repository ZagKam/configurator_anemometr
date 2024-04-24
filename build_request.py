from get_crc import get_crc


def build_request(request: str) -> bytes:
    """
    Функция для формирования байтового запроса.
    
    Аргументы:
        - request: str запрос без контрольной суммы;
    
    Возвращает:
        - bytes сформированный запрос с контрольной суммой.
    """
    try:
        return bytes.fromhex(request + get_crc(request))
    except ValueError as e:
        print(f"Error in build_request: {e} request:{request}, crc:{get_crc(request)}")
        return b''  # Возвращаем пустой объект байтов в случае ошибки
