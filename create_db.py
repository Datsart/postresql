from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime
import psycopg2 # для коннекта
from datetime import datetime

# Строка подключения к базе данных
db_url = 'postgresql://artemdatsenko:19980723@localhost:5432/log_info' # для движка

# Устанавливаем соединение с базой данных PostgreSQL
conn = psycopg2.connect(
    database="log_info", user='artemdatsenko', password='19980723', host='localhost', port='5432'  # для курсора
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
metadata.create_all(engine)

