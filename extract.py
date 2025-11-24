
# Импортируем библиотеки
import imaplib
import config
import email
from email.header import decode_header
import pandas as pd 
import re

from mail_parser import extract_msg_body

def extract():
    # Получение данных для авторизации из конфиг-файла
    username = config.username # Имя пользователя / логин
    password = config.password # Пароль
    imap_server = 'imap.gmail.com' # Адрес почтового сервера

    # Подключение к серверу через протокол SSL
    imap = imaplib.IMAP4_SSL(imap_server)

    # Авторизация при помощи логина и пароля
    imap.login(user=username, password=password)

    # Выбор папки с входящими письмами
    imap.select('INBOX')

    # Поиск всех непрочитанных писем
    status, mail_ids = imap.search(None, '(X-GM-LABELS "Purchases")')

    # Переведем строку в список (list)
    mail_ids_list = mail_ids[0].split()

    # Выведем полученный список
    print(f'Непрочитанные письма: {mail_ids_list}')

    # А также количество полученных писем
    print(f'Количество непрочитанных писем: {len(mail_ids_list)}')

    # Запишем информацию из писем в Датафрейм
    # В качестве колонок Датафрейма выберем ID, получателя письма, имя отправителя,
    # почтовый адрес отправителя, дату получения письма, цену покупки и валюту
    df = pd.DataFrame(columns=['ID', 'Receiver', 'Sender Name', 'Sender Mail', 'Date', 'Price', 'Currency'])
    for id in mail_ids_list:
        # Извлекаем письмо по ID
        res, msg_data = imap.fetch(id, '(RFC822)')
        raw_email = msg_data[0][1]
        # Преобразуем байты в объект сообщения
        msg = email.message_from_bytes(raw_email)
        
        # Для извлечения цены из тела письма используем регулярное выражение
        price_pattern = r'(?:\d+[.,]?\d*[,.]?\d*\s*RUB|RUB\s*\d+[.,]?\d*[,.]?\d*)'
        prices = re.findall(price_pattern, extract_msg_body(msg), re.IGNORECASE)

        # Записываем данные из письма в Датафрейм
        df.loc[len(df)] = {'ID': int(len(df)), \
                            'Receiver': msg["To"], \
                            'Sender Name': msg["From"], \
                            'Date': msg["Date"], \
                            'Price': (prices or [None])[-1] } #В качестве цены берем последнее значение
        
                
    return df