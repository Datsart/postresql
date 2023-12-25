import random
from faker import Faker
from datetime import datetime
from flask import Flask, request, jsonify
import pandas as pd
import numpy

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
    unique_countries_count = df['country'].nunique()  # Количество уникальных стран в выборке

    ################################ ВТОРОЕ ЗАДАНИЕ
    total_deposits_by_country = df.groupby('country')['deposit'].sum()  # группируем страны
    country_with_max_deposits = total_deposits_by_country.idxmax()  # страна где больше всего депозитов

    ################################ ТРЕТЬЕ ЗАДАНИЕ
    client_email_counts = df.groupby('id')['email'].nunique()

    clients_with_multiple_emails = client_email_counts[
        client_email_counts > 1]  ## фильтруем только тех клиентов, у которых больше 1 email

    # получаем количество клиентов с более чем 1 email
    num_clients_with_multiple_emails = len(clients_with_multiple_emails)

    ################################ ЧЕТВЕРТОЕ ЗАДАНИЕ
    client_country_counts = df.groupby('id')['country'].nunique()

    clients_in_multiple_countries = client_country_counts[client_country_counts > 1]

    num_clients_in_multiple_countries = len(clients_in_multiple_countries)

    ################################  ПЯТОЕ ЗАДАНИЕ
    df['expenses_ratio'] = df['costs'] / df['deposit']

    max_ratio_client = df.loc[df['expenses_ratio'].idxmax()]

    email_max_ratio_client = max_ratio_client['email']
    return jsonify({"data_size": size})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
