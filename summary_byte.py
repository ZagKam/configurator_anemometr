



def sum_byte(num1, num2):
    # Преобразуем числа в байты в шестнадцатеричном формате
    byte1 = bytes([num1])
    byte2 = bytes([num2])

    # Объединяем байты в один байт
    combined_byte = byte1 + byte2

    # Преобразуем объединенный байт в число
    result = int.from_bytes(combined_byte, byteorder='big')
    return(result)