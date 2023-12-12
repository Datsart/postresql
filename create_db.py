from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime, delete
import psycopg2  # для коннекта с постгрес
from datetime import datetime

conn = psycopg2.connect(
    database='postgres',
    user='artemdatsenko',
    password='19980723',
    host='localhost',
    port='5432'
)  # первый коннект, подключение к стоковой БД
conn.autocommit = True
cursor = conn.cursor()

db_name = 'log_info'  # НАЗВАНИЕ НОВОЙ ИЛИ СТАРОЙ БД

# Проверяем существование базы данных
cursor.execute(f"SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = '{db_name}')")
db_exists = cursor.fetchone()[0]

# Если базы данных не существует, создаем новую
if not db_exists:

    cursor.execute(f"CREATE DATABASE {db_name}")
    print(f"Создана база данных '{db_name}'")
else:
    print(f"База данных '{db_name}' уже существует")

    # Подключаемся к новой базе данных
conn = psycopg2.connect(
    database=f'{db_name}',
    user='artemdatsenko',
    password='19980723',
    host='localhost',
    port='5432'
)
conn.autocommit = True
#  проверка на существование таблицы
cursor = conn.cursor()
table_name = 'api_data'  # НАЗВАНИЕ НОВОЙ ИЛИ СТАРОЙ ТАБЛИЦЫ
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS public.api_data (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        value INTEGER
    )
    """
)
print(f"Таблица '{table_name}' успешно создана.")
# Проверка наличия данных в таблице
cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
row_count = cursor.fetchone()[0]

# Если таблица содержит данные, выполняем TRUNCATE TABLE
if row_count > 0:
    cursor.execute(f"TRUNCATE TABLE {table_name}")
    print(f"Таблица '{table_name}' успешно очищена.")
else:
    print(f"Таблица '{table_name}' не содержит данных. TRUNCATE не выполнен.")
# exists = cursor.fetchone()[0]

# metadata = MetaData()
# info = Table(f'{table_name}', metadata,
#              Column('id', Integer, primary_key=True, unique=True),
#              Column('timestamp', DateTime(), default=datetime.now),
#              Column('value', Integer),
#              )
# db_url = 'postgresql://artemdatsenko:19980723@localhost:5432/log_info'  # для движка
# engine = create_engine(db_url)  # движок
# connection = engine.connect()  # подключение к БД
# if exists is False:
#
#     # Создаем таблицу 'api_data' в базе данных
#     metadata.create_all(engine)  # добавили в бд
#     connection.commit()
# else:
#     print('Такая таблица уже создана и очистили значения полей')
#     # удаление значений
#     delete_stmt = delete(info)
#     connection.execute(delete_stmt)
#     connection.commit()
# # Закрываем соединение
cursor.close()
conn.close()
