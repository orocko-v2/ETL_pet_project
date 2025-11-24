import base64
def extract_msg_body(message):
    """Функция для извлечения содержимого письма 
    с возможностью обработки вложенных сообщений. 

    Args:
        message (list): Объект сообщения

    Returns:
        body (str): Содержимое письма
    """

    # Если письмо содержит вложенные элементы
    if message.is_multipart():
        # Проходим по частям письма
        for part in message.walk():
            ctype = part.get_content_type()
            cdisposition = part.get('Content-Disposition')
            # Если часть письма - текст
            if (ctype == 'text/plain' or ctype == 'text/html') \
                and 'attachment' not in str(cdisposition):
                try:
                    # Раскодируем содержимое
                    body = part.get_payload(decode=True).decode()
                    return body   
                except UnicodeDecodeError:
                    # При ошибке пробуем другую кодировку
                    body = part.get_payload(decode=True).decode('latin-1')
                    return body

    else:
        # Если письмо не содержит вложенных частей
        try:
            # Раскодируем содержимое
            body = message.get_payload(decode=True).decode()
            return body
        except UnicodeDecodeError:
            # При ошибке пробуем другую кодировку
            body = message.get_payload(decode=True).decode('latin-1')
            return body
        