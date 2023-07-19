import requests

obj = {"0_0":"red"}
print(obj)
req = requests.post(url="localhost:5000/post", data=obj)