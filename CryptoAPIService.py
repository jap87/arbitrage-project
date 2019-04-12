import http.client
import json
from flask import Flask
import time
from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship

graph = Graph("bolt://localhost:7687", auth=("neo4j", "juanjulian"))
tx = graph.begin()
graph.schema.create_uniqueness_constraint("Currency","name")

# app = Flask(__name__)
# time.sleep(5)
# print("hello")
# check out http://docs.nomics.com for the list of routes and what they give you and what parameters they require
connection = http.client.HTTPSConnection('api.nomics.com')
connection.request("GET", "/v1/exchange-markets/prices?key=fd24ac27f03b5016a3a44e8179d6da86")
response = connection.getresponse()
list_of_exchange = json.loads(response.read())

print(list_of_exchange[0])
unique_names = set()
for i in list_of_exchange:
    first_node = graph.nodes.match("Currency", name=i["base"]).first()
    second_node = graph.nodes.match("Currency", name=i["quote"]).first()
    relationship = Relationship(first_node,"Buys",second_node,cost=i["price_quote"],timestamp=i["timestamp"])
    tx.create(relationship)

tx.commit()
# first_node = Node("Currency",name=list_of_exchange[0]["base"])
# tx.create(first_node)
# second_node = Node("Currency",name=list_of_exchange[0]["quote"])
# tx.create(second_node)
# relationship = Relationship(first_node,"Buys",second_node,cost=list_of_exchange[0]["price_quote"],timestamp=list_of_exchange[0]["timestamp"])
# tx.create(relationship)
# tx.commit()

connection.close()