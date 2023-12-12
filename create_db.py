from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime
import psycopg2 # для коннекта
from datetime import datetime

name_db = str(input('Введите название БД: '))
dialect = str(input('Введите диалект: '))
user = str(input('Введите юзера: '))
password = str(input('Введите пароль: '))
host = str(input('Введите хост: '))
port = str(input('Введите порт: '))

# Строка подключения к базе данных
db_url = f'{dialect}://{user}:{password}@{host}:{port}/{name_db}' # для движка

# Устанавливаем соединение с базой данных PostgreSQL
conn = psycopg2.connect(
    database=f'{name_db}', user=f'{user}', password=f'{password}', host=f'{host}', port=f'{port}'  # для курсора
)
conn.autocommit = True  # Устанавливаем автоматический режим подтверждения транзакций

# Создаем объект метаданных для работы с SQLAlchemy
metadata = MetaData()

# Определяем структуру таблицы 'api_data'
info = Table('api_data', metadata,
             Column('id', Integer, primary_key=True, unique=True),
             Column('timestamp', DateTime(), default=datetime.now),
             Column('value', Integer),
             )

# Создаем движок (engine) для работы с SQLAlchemy
engine = create_engine(db_url, echo=True)  # Параметр echo=True выводит SQL-запросы в консоль

# Пытаемся установить соединение с базой данных
connection = engine.connect()
print("Подключение успешно установлено.")

# Создаем таблицу 'api_data' в базе данных
# metadata.create_all(engine)

cursor = conn.cursor()
cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = 'log_info')")
exists = cursor.fetchone()[0] # здесь True или False
print(exists)

if exists is not True:
    name_db = str(input('Введите название БД: '))
    cursor.execute(f'CREATE DATABASE {name_db}')
    print(f'Создана база данных {name_db}')