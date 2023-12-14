from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database

user = str(input('Введите имя пользователя: ')).strip()
password = str(input('Введите пароль: ')).strip()
host = str(input('Введите хост: ')).strip()
port = str(input('Введите порт: ')).strip()
name_db = str(input('Введите имя начальной БД: ')).strip()


def create_connection(user, password, host, port, name_db):
    """Вспомогательная функция создания соединения с БД"""

    alchemyEngine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{name_db}')
    dbConnection = alchemyEngine.connect()
    return dbConnection


# первое подключение к стоковой БД
dbConnection = create_connection(user, password, host, port, name_db)

# dbConnection = create_connection('postgresql://artemdatsenko:19980723@localhost:5432/log_info')

# проверка и создание новой БД
new_db_name = 'log_info'

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{new_db_name}')

if not database_exists(engine.url):  # проверка на существование БД
    create_database(engine.url)
    print(f'Создана БД {new_db_name}')
else:
    print('Такая БД уже есть')

# Создание подключения на новую БД
dbConnection = create_connection(user, password, host, port, new_db_name)

#  проверка на существование таблицы
table_exists = engine.dialect.has_table(dbConnection, 'api_data')

if table_exists:
    truncate_sql = text('TRUNCATE TABLE public.api_data RESTART IDENTITY CASCADE')
    dbConnection.execute(truncate_sql)
    dbConnection.commit()
    print('Такая таблица уже есть - очистили значения')

else:
    create_table_sql = """
        CREATE TABLE public.api_data (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            value INTEGER
        )
    """
    dbConnection.execute(text(create_table_sql))
    dbConnection.commit()
    print('Создана таблица api_data')
dbConnection.close()
