import requests
import random
import json

headers = {
    'Content-Type': 'application/json'
}
# counter = 1
# payload = json.dumps({
#     "data_size": 1,
#     'hash': counter
# })
# counter += 1
# response = requests.post("http://127.0.0.1:5050/training_model", data=payload, headers=headers)
response = requests.post("http://127.0.0.1:5050/training_model", headers=headers)
print(response.json())
