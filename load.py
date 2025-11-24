import psycopg2
import config

def load_data_to_temp_table():
    """
    Загрузка данных из CSV в таблицу.
    """

    # Подключаемся к базе данных
    try:
        with psycopg2.connect(
            database=config.db_name,
            user=config.db_user,
            password=config.db_password,
            host=config.db_host,
            port=config.db_port
        ) as conn:
            # Открываем курсор для выполнения SQL-запросов
            with conn.cursor() as cur, open('data/emails.csv', 'r', encoding='utf-8') as file:
                # Создаем таблицу, если она не существует
                create_table_query = """
                    CREATE TABLE IF NOT EXISTS emails (
                        ID INT PRIMARY KEY,
                        receiver VARCHAR(255) NOT NULL,
                        sender_name VARCHAR(255) NOT NULL,
                        sender_mail VARCHAR(255) NOT NULL,
                        date DATE NOT NULL,
                        price DECIMAL(10, 3),
                        currency VARCHAR(8)
                    );
                    """
                cur.execute(create_table_query)
                # Загружаем данные из CSV в таблицу базы данных
                cur.copy_from(file, 'emails', sep=';', null='None')
                conn.commit()  # Подтверждаем транзакцию
                print("Данные успешно загружены")
    except psycopg2.OperationalError as err:
        pass