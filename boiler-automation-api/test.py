import requests
from time import sleep

BASE = "http://127.0.0.1:5000/"

# response = requests.put(BASE + "data", {"temperature": "48.9"})
# print(response)

# sleep(2)

# response = requests.put(BASE + "data", {"temperature": "50"})
# print(response)

# sleep(2)

# response = requests.put(BASE + "data", {"temperature": "45.3"})
# print(response)

response = requests.get(BASE + "data")
print(response.json())

response = requests.get(BASE + "status")
print(response.json())

response = requests.post(BASE + "status", {"state": "off"})
print(response.json())

response = requests.get(BASE + "status")
print(response.json())
