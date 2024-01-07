from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from healthcheck import HealthCheck
import random
from faker import Faker
from datetime import datetime, timezone
import pandas as pd
import numpy
import time
import csv
import subprocess
import os

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


current_process = None


@app.route('/training_model', methods=['POST', "GET"])
def training_model():
    global current_process

    if current_process and current_process.poll() is None:
        df = pd.DataFrame({
            'message': ['Подождите завершения предыдущего процесса'],
            'hash': [1],
            'datetime': [f'{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}']
        })

        df.to_csv('result.csv', mode='a', header=False, index=False)
        return jsonify({"message": "Подождите завершения предыдущего процесса",
                        "hash": 1,
                        'time': f'{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}'})

    process = subprocess.Popen(["python3", "training.py", "5"])

    current_process = process
    df = pd.DataFrame({
        'message': ['Процесс запущен'],
        'hash': [0],
        'datetime': [f'{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}']
    })

    df.to_csv('result.csv', mode='a', header=False, index=False)
    return jsonify({"message": "Процесс запущен",
                    "hash": 0,
                    'time': f'{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}'
                    })


@app.route('/get_stat', methods=['POST'])
def get_stat():
    data = request.get_json()
    value = int(data['hash_id'])
    return jsonify({"hash_id": value})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
