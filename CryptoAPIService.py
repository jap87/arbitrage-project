import http.client
import json

# check out http://docs.nomics.com for the list of routes and what they give you and what parameters they require
connection = http.client.HTTPSConnection('api.nomics.com')
connection.request("GET", "/v1/markets?key=fd24ac27f03b5016a3a44e8179d6da86")
response = connection.getresponse()
# the /markets API route returns a list of markets that this API keeps track of.
# this line takes the response from the server and turns it into a python list
list_of_markets = json.loads(response.read())
print(list_of_markets[0])
print(list_of_markets[1])

connection.close()