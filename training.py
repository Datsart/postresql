import random
from faker import Faker
from datetime import datetime
from flask import Flask, request, jsonify
import pandas as pd
import numpy
import time
numpy.random.seed(22)
fake = Faker()

app = Flask(__name__)


@app.route('/training_model', methods=['POST'])
def send_data_size():
    data = request.get_json()
    size = int(data['data_size'])

    # print(size)  # в size наше число

    def generate_data():
        result = []
        # вместо range - data_size
        for i in range(size):
            email = fake.email()
            id = random.randint(0, 100)
            deposit = random.randint(0, 10_000)
            costs = random.randint(0, 10_000)
            countries_list = ['Россия', 'Казахстан', 'США', 'Германия', 'Канада']
            country = random.choice(countries_list)
            date = fake.date_this_year()

            formatted_date = datetime.strftime(date, "%Y-%m-%d")

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

    df = pd.DataFrame(generate_data())  # в рез-те работы функции у нас список словарей

    ################################ ПЕРОЕ ЗАДАНИЕ
    unique_countries = len(df.country.unique())  # Количество уникальных стран в выборке
    time.sleep(5)
    ################################ ВТОРОЕ ЗАДАНИЕ
    deposits_sum = df.groupby('country')['deposit'].sum()  # группируем страны
    country_max_deposits = deposits_sum.idxmax()  # страна где больше всего депозитов
    time.sleep(5)
    ################################ ТРЕТЬЕ ЗАДАНИЕ
    email_count = df.groupby('id')['email'].nunique()

    clients_with_emails = email_count[
        email_count > 1]  ## фильтруем только тех клиентов, у которых больше 1 email

    # получаем количество клиентов с более чем 1 email
    clients_count_email = len(clients_with_emails)
    time.sleep(5)
    ################################ ЧЕТВЕРТОЕ ЗАДАНИЕ
    country_count = df.groupby('id')['country'].nunique()

    clients_countries = country_count[country_count > 1]

    clients_count_countries = len(clients_countries)

    ################################  ПЯТОЕ ЗАДАНИЕ
    df['expenses_ratio'] = df['costs'] / df['deposit'] # создали новый столбец

    max_ratio_client = df.loc[df['expenses_ratio'].idxmax()] # достали клиента с max 

    email_max_ratio_client = max_ratio_client['email']
    time.sleep(5)
    return jsonify({"data_size": size})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
