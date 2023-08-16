import requests

baseurl = "https:/127.0.0.1:5000/"

response = requests.get(baseurl+"helloworld")
print(response.json())