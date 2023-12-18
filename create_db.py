from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database, drop_database

DB_URI = 'postgresql://artemdatsenko:19980723@localhost:5432/log_info'
if database_exists(DB_URI):
    drop_database(DB_URI)

create_database(DB_URI)
print('Создана новая БД')


def create_connection():
    """Вспомогательная функция создния соединения с БД"""
    alchemyEngine = create_engine(DB_URI)
    dbConnection = alchemyEngine.connect()
    return dbConnection


dbConnection = create_connection()

sql = """
    CREATE TABLE IF NOT EXISTS public.api_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    value VARCHAR(255) NOT NULL)
"""
dbConnection.execute(text(sql))
dbConnection.commit()
dbConnection.close()
print('Создана новая таблица')
