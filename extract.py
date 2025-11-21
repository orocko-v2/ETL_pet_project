
# Импортируем библиотеки
import imaplib
import config
import email
from email.header import decode_header

from mail_parser import extract_msg_body

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
status, mail_ids = imap.search(None, 'UNSEEN')

# Переведем строку в список (list)
mail_ids_list = mail_ids[0].split()

# Выведем полученный список
print(f'Непрочитанные письма: {mail_ids_list}')

print(f'Количество непрочитанных писем: {len(mail_ids_list)}')

id = mail_ids_list[0]
res, msg_data = imap.fetch(id, '(RFC822)')
raw_email = msg_data[0][1]
msg = email.message_from_bytes(raw_email)

print('\nЗаголовок письма:\n', decode_header(msg["Subject"])[0][0].decode())

print(extract_msg_body(msg))

