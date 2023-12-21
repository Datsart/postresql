import requests
import random
import json

headers = {
    'Content-Type': 'application/json'
}
payload = json.dumps({
    "score": round(random.random(), 2)
})

response = requests.post("http://127.0.0.1:5050/sendmsg", data=payload, headers=headers)
print(response.json())
