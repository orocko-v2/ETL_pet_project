from extract import extract
from transform import str_to_datetime, transform
import pandas as pd
from load import load_data_to_temp_table

def main():
    # Выгрузка данных из почтового сервера 
    df = extract() 
    # Изменение данных
    df = transform(df)
    pd.set_option('display.max_columns', None)
    # Вывод полученного Датафрейма
    print(df)
    # Запись данных в .csv файл 
    df.to_csv('data/emails.csv', sep=';', encoding='utf-8', index=False, header=False)
    # Загрузка данных в таблицу
    load_data_to_temp_table()
    
if __name__ == '__main__':
    main()
    