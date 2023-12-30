import random
from faker import Faker
from datetime import datetime, timezone
import pandas as pd
import numpy
import time
import sys

numpy.random.seed(22)
fake = Faker()


def generate_data(size):
    result = []
    for i in range(int(size)):
        email = fake.email()
        id = random.randint(0, 100)
        deposit = random.randint(0, 10_000)
        costs = random.randint(0, 10_000)
        countries_list = ['Россия', 'Казахстан', 'США', 'Германия', 'Канада']
        country = random.choice(countries_list)
        date = fake.date_this_year()

        formatted_date = datetime.strftime(date, "%Y-%m-%d %H:%M:%S")

        data_dict = {
            'email': email,
            'id': id,
            'deposit': deposit,
            'costs': costs,
            'country': country,
            'date': formatted_date,
        }
        result.append(data_dict)
    return result


def result_metrics():
    df = pd.DataFrame(generate_data(size))
    value_time = 5
    ################################ ПЕРОЕ ЗАДАНИЕ
    unique_countries = len(df['country'].unique())  # Количество уникальных стран в выборке
    time.sleep(value_time)
    ################################ ВТОРОЕ ЗАДАНИЕ
    deposits_sum = df.groupby('country')['deposit'].sum()  # группируем страны
    country_max_deposits = deposits_sum.idxmax()  # страна где больше всего депозитов
    time.sleep(value_time)
    ################################ ТРЕТЬЕ ЗАДАНИЕ
    email_count = df.groupby('id')['email'].nunique()

    clients_with_emails = email_count[
        email_count > 1]  # фильтруем только тех клиентов, у которых больше 1 email

    # получаем количество клиентов с более чем 1 email
    clients_count_email = len(clients_with_emails)
    time.sleep(value_time)
    ################################ ЧЕТВЕРТОЕ ЗАДАНИЕ
    country_count = df.groupby('id')['country'].nunique()

    clients_countries = country_count[country_count > 1]

    clients_count_countries = len(clients_countries)

    ################################  ПЯТОЕ ЗАДАНИЕ
    df['expenses_ratio'] = df['costs'] / df['deposit']  # создали новый столбец

    max_ratio_client = df.loc[df['expenses_ratio'].idxmax()]  # достали клиента с max

    email_max_ratio_client = max_ratio_client['email']
    time.sleep(value_time)

    df = pd.DataFrame({
        'feature': ['Страна в которой больше всего осталось депозитов'],
        'value': [country_max_deposits],
        'datetime': [datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")]
    })

    df.to_csv('result.csv', mode='a', header=False, index=False)
    print('Операция выполнена')


size = sys.argv[1]
result_metrics()
