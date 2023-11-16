import datetime

import networkx as nx

from .graph_builder import build_graph
from .graph_algorithms import group_elements, determine_end
from .graph_builder_x import build_graph_x
from .graph_algorithms_x import order_graph

static_param1 = "value1"
static_param2 = "value2"

# Create the graph during package initialization
graph = build_graph(static_param1, static_param2)
graph = group_elements(graph)
graph = determine_end(graph)

graph_data = order_graph(build_graph_x())
print("----------------ÖÖ--------------------")
for data in graph_data["nodes"]:
    print(data["start"], data["speaker"], data["text"])
print("----------------ÖÖ--------------------")

print("--------------------------------------")
for start_time, globalNodeID, graphEdges, speaker, text, texts, end_time in graph:
    print(start_time, speaker, text)
print("--------------------------------------")

#print("--------------------------------------")
#for data in graph_data["nodes"]:
#    print(data["start"], data["speaker"], data["text"])
#print("--------------------------------------")

