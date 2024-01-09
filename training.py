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
    counter = 0
    for j in range(int(size) * 5):  # 5 - количество метрик
        df = pd.DataFrame(generate_data(size))
        value_time = 0
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
        df = pd.DataFrame({
            'hash': [hash_date.hexdigest()],
            'feature': [name_metrics[counter]],
            'value': [value_metrics[counter]],
            'datetime': [date]
        })
        counter += 1
        if counter >= 5:
            counter = 0

        if os.path.exists('result.csv'):
            df.to_csv('result.csv', mode='a', header=False, index=False)
        else:
            df.to_csv('result.csv', mode='a', header=True, index=False)

    print('Операция выполнена')


try:
    size = sys.argv[1]
    date_term = sys.argv[2]
    hash_date_term = sys.argv[3]
    result_metrics(size, date_term, hash_date_term)
except IndexError:
    size = sys.argv[1]
    result_metrics(size)
