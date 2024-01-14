import requests
import random
import json


def sendmsg():
    headers = {
        'Content-Type': 'application/json'
    }

    url = "http://127.0.0.1:5050/sendmsg"

    payload = json.dumps({"score": round(random.random(), 2)})

    response = requests.post(url, data=payload, headers=headers)
    print(response.text)
    return f'{response.text}'


# sendmsg()

def healthcheck():
    url = "http://127.0.0.1:5050/healthcheck"
    response = requests.get(url)
    print(response.text)
    return f'{response.text}'


# healthcheck()
def training_model(size):
    url = "http://127.0.0.1:5050/training_model"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {"size": size}

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return f'{response.json()}'


training_model(432)
