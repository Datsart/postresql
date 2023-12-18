import requests
import random

response = requests.post("http://127.0.0.1:5050/sendmsg", data={"score": round(random.uniform(0, 1), 2)})
print(response.json())
