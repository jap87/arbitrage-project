import http.client
import json

connection = http.client.HTTPSConnection('api.nomics.com')
connection.request("GET", "/v1/exchange-markets/prices?key=fd24ac27f03b5016a3a44e8179d6da86")
response = connection.getresponse()

list_of_exchange = json.loads(response.read())
unique_names = set()
for i in list_of_exchange:
    unique_names.add(i["base"])
    unique_names.add(i["quote"])
    
unique_names = set()
for i in list_of_exchange:
    unique_names.add(i["base"])
    unique_names.add(i["quote"])