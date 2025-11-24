from datetime import datetime
from email.header import decode_header
import base64, re

def str_to_datetime(str_date: str):
    """Преобразует строку в переменную формата datetime

    Args:
        str_date (str): строка с датой

    Returns:
        dateobj (datetime): объект datetime
    """
    
    try:
        # Формат строки даты
        format = '%a, %d %b %Y %H:%M:%S %z'
        # Переводим строку в datetime
        dateobj = datetime.strptime(str_date, format)
        return dateobj
    except ValueError:
        pass        
    try:
        # Другой формат строки даты
        format = '%a, %d %b %Y %H:%M:%S %z (%Z)'
        # Переводим строку в datetime
        dateobj = datetime.strptime(str_date, format)
        return dateobj
    except ValueError:
        pass


def transform(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Паттерн для разделения цены и валюты
    pattern = r'\s*(?P<amount>\d+[.,]?\d*[,.]?\d*)\s*\xa0*(?P<currency>[A-Z]{3})|\s*(?P<currency2>[A-Z]{3})\s*\xa0*(?P<amount2>\d+[.,]?\d*[,.]?\d*)'
    # Проходимся по рядам Датафрейма
    for index, row in df.iterrows():
        # В колонке получателя убираем кавычки и переводим в нижний регистр
        df.at[index, 'Receiver'] = row['Receiver'].replace('<', '').replace('>', '').\
            replace('\"', '').lower()
        # Разделяем отправителя на имя и почтовый адрес
        sender = row['Sender Name'].split('<')
        df.at[index, 'Sender Name'] = sender[0][:-1].replace('\"', '')
        df.at[index, 'Sender Mail'] = sender[1][:-1] 
        # Переводим дату в формат datetime с помощью соответствующей функции  
        df.at[index, 'Date'] = str_to_datetime(row['Date'])
        # Разделяем цену на число и валюту
        if row['Price'] is not None:
            match = re.search(pattern, row['Price'])
            amount = match.group('amount') or match.group('amount2')
            currency = match.group('currency') or match.group('currency2')
            amount = amount.replace(',', '.')
            # Удаляем точки, разделяющие разряды
            df.at[index, 'Price'] = float(amount.replace('.', '', amount.count('.') - 1))
            df.at[index, 'Currency'] = currency
        else:
            df.at[index, 'Price'] = 'None'
            df.at[index, 'Currency'] = 'None'
    return df

    