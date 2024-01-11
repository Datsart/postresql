import os.path
import random
from faker import Faker
from datetime import datetime, timezone
import pandas as pd
import numpy
import time
import sys
import hashlib
import logging

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


def result_metrics(*args, **kwargs):
    df = pd.DataFrame(generate_data(size))
    value_time = 0

    ################################ ПЕРОЕ ЗАДАНИЕ
    unique_countries = df['country'].nunique()  # Количество уникальных стран в выборке
    time.sleep(value_time)

    ################################ ВТОРОЕ ЗАДАНИЕ
    country_max_deposits = df.groupby('country', as_index=False).aggregate({'deposit': 'sum'}).sort_values(
        'deposit', ascending=False).iloc[0]['country']  # страна где больше всего депозитов
    time.sleep(value_time)

    ################################ ТРЕТЬЕ ЗАДАНИЕ
    a = df.groupby('id')['email'].nunique() > 1
    clients_count_email = len(a[a == True])  # количество клиентов у которых больше чем 1 email
    time.sleep(value_time)

    ################################ ЧЕТВЕРТОЕ ЗАДАНИЕ
    a = df.groupby('id')['country'].nunique() > 1
    clients_count_countries = len(a[a == True])
    ################################  ПЯТОЕ ЗАДАНИЕ
    group_sum_dataframe = df.groupby('email').aggregate({'costs': 'sum', 'deposit': 'sum'})
    group_sum_dataframe['max_dolya'] = group_sum_dataframe['costs'] / group_sum_dataframe['deposit']
    email_max_ratio_client = group_sum_dataframe.sort_values(by=['max_dolya'], ascending=False).index[0]
    time.sleep(value_time)

    name_metrics = ['Количество уникальных стран в выборке',
                    'Страна в которой больше всего осталось депозитов у клиентов',
                    'Количество клиентов у которых больше 1 email в выборке',
                    'Количество клиентов  которые присутствуют больше чем в 1 стране',
                    'Email клиента с максимальной долей трат от депозита']
    value_metrics = [unique_countries,
                     country_max_deposits,
                     clients_count_email,
                     clients_count_countries,
                     email_max_ratio_client]

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    hash_date = hashlib.md5(date.encode())
    if 'date_term' and 'hash_date_term' in locals():
        date = date_term
        hash_date = hashlib.md5(date.encode())

    _dict = {'hash': [hash_date.hexdigest()] * 5,
             'feature': ['Количество уникальных стран в выборке',
                         'Страна в которой больше всего осталось депозитов у клиентов',
                         'Количество клиентов у которых больше 1 email в выборке',
                         'Количество клиентов  которые присутствуют больше чем в 1 стране',
                         'Email клиента с максимальной долей трат от депозита'],
             'value': [unique_countries, country_max_deposits, clients_count_email, clients_count_countries,
                       email_max_ratio_client],
             'datetime': [date] * 5,
             }
    df = pd.DataFrame(_dict)
    if os.path.exists('result.csv'):
        df.to_csv('result.csv', mode='a', header=False, index=False)
    else:
        df.to_csv('result.csv', mode='a', header=True, index=False)

    print('Операция выполнена')


try:
    size = int(sys.argv[1])
    date_term = sys.argv[2]
    hash_date_term = sys.argv[3]
    result_metrics(size, date_term, hash_date_term)
except IndexError:
    size = int(sys.argv[1])
    result_metrics(size)
