from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from healthcheck import HealthCheck
import random
from faker import Faker
from datetime import datetime
import pandas as pd
import numpy
import time
import csv

numpy.random.seed(22)
fake = Faker()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://artemdatsenko:19980723@localhost:5432/log_info'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

health = HealthCheck()


class LogInfo(db.Model):
    __tablename__ = 'api_data'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    value = db.Column(db.Float, nullable=False)


@app.route('/sendmsg', methods=['POST'])
def send_message():
    # score = request.form.get('score')
    data = request.get_json()
    score = float(data['score'])
    log_info = LogInfo(value=score)
    db.session.add(log_info)
    db.session.commit()

    return jsonify({"score": score})


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    health_status = health.run()
    return jsonify({"healthcheck": health_status})


@app.route('/training_model', methods=['POST'])
def send_data_size():
    data = request.get_json()
    size = int(data['data_size'])
    counter = int(data['hash'])

    # print(size)  # в size наше число

    def generate_data():
        result = []
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
    # time.sleep(5)
    ################################ ВТОРОЕ ЗАДАНИЕ
    deposits_sum = df.groupby('country')['deposit'].sum()  # группируем страны
    country_max_deposits = deposits_sum.idxmax()  # страна где больше всего депозитов
    # time.sleep(5)
    ################################ ТРЕТЬЕ ЗАДАНИЕ
    email_count = df.groupby('id')['email'].nunique()

    clients_with_emails = email_count[
        email_count > 1]  ## фильтруем только тех клиентов, у которых больше 1 email

    # получаем количество клиентов с более чем 1 email
    clients_count_email = len(clients_with_emails)
    # time.sleep(5)
    ################################ ЧЕТВЕРТОЕ ЗАДАНИЕ
    country_count = df.groupby('id')['country'].nunique()

    clients_countries = country_count[country_count > 1]

    clients_count_countries = len(clients_countries)

    ################################  ПЯТОЕ ЗАДАНИЕ
    df['expenses_ratio'] = df['costs'] / df['deposit']  # создали новый столбец

    max_ratio_client = df.loc[df['expenses_ratio'].idxmax()]  # достали клиента с max

    email_max_ratio_client = max_ratio_client['email']
    # time.sleep(5)

    df = pd.DataFrame({
        'hash': [counter],
        'feature': ['Страна в которой больше всего осталось депозитов'],
        'value': [country_max_deposits],
        'datetime': [datetime.utcnow()]
    })

    df.to_csv('result.csv', mode='a', header=False, index=False)

    return jsonify({"data_size": size, 'hash': counter})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
