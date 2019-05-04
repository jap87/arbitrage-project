import http.client
import json
from flask import Flask
import time
import hashlib
import math
from py2neo import Graph, Node, Relationship

from dag_detect import simple_cycles

# graph = Graph("bolt://vcm-8793.vm.duke.edu:7687", auth=("neo4j", "juanjulian"))
graph = Graph("bolt://vcm-8793.vm.duke.edu:7687", auth=("neo4j", "juanjulian"))
tx = graph.begin()
#graph.schema.create_uniqueness_constraint("Currency","name")

# check out http://docs.nomics.com for the list of routes and what they give you and what parameters they require
connection = http.client.HTTPSConnection('api.nomics.com')
connection.request("GET", "/v1/exchange-markets/prices?key=fd24ac27f03b5016a3a44e8179d6da86")
response = connection.getresponse()
list_of_exchange = json.loads(response.read())

unique_names = dict()
unique_bases = set()
G = dict()

#TODO: Remove duplicate edges
counter = 0
for i in list_of_exchange:
    if(i["quote"] not in unique_names.keys()):
        unique_names[i["quote"]] = counter
        counter += 1
    if(i["base"] in unique_bases):
        G[unique_names[i["base"]]].append(unique_names[i["quote"]])
    else:
        if(i["base"] not in unique_names.keys()):
            unique_names[i["base"]] = counter
            unique_bases.add(i["base"])
            counter += 1
        else:
            unique_bases.add(i["base"])
        G[unique_names[i["base"]]] = [unique_names[i["quote"]]]

print(G)
filtered_list = []


# for i in unique_names:
#     node = Node("Currency",name=i)
#     tx.create(node)
# tx.commit()


print(tuple(simple_cycles(G)))

# for i in filtered_list:
#     first_node = graph.nodes.match("Currency", name=i["base"]).first()  
#     second_node = graph.nodes.match("Currency", name=i["quote"]).first()
#     print(first_node, second_node)
#     relationship = Relationship(first_node,"Buys",second_node,cost=math.log(float(i["price_quote"])),timestamp=i["timestamp"])
#     tx.create(relationship)
# tx.commit()

# arbitrage = graph.run("MATCH p=(n)-[r1:DISTANCE]->()-[r2:DISTANCE]->()-[r3:DISTANCE]->(n) WHERE r1.dist + r2.dist+r3.dist <> 0 RETURN p").to_subgraph().relationships
# for i in arbitrage:
#     print(str(i,-2))
# S = set()

connection.close()