#import ogdf_python
from datetime import datetime
import json
import os

graphNodes = []
#json_folder_path = 'C:/Users/Martin Gruber/OneDrive - gw.uni-passau.de/Studium/7. Semester/Bachelorarbeit/Data/qt30'  # may not sty here


json_folder_path = 'C:/Users/Martin Gruber/OneDrive - gw.uni-passau.de/Studium/7. Semester/Bachelorarbeit/Data/qt30'  # may not sty here

def build_graph(param1, param2):  # the parameters are about to be channged to e.g. speaker list and path to folder
    json_file_path = 'C:/Users/Martin Gruber/OneDrive - gw.uni-passau.de/Studium/7. Semester/Bachelorarbeit/Data/qt30/nodeset17957.json'
    # json_file_path = 'C:/Users/grube/OneDrive - gw.uni-passau.de/Studium/7. Semester/Bachelorarbeit/Data/qt30/nodeset17932.json'
    # json_file_path = 'C:/Users/Martin Gruber/OneDrive - gw.uni-passau.de/Studium/7. Semester/Bachelorarbeit/Data/qt30/nodeset17925.json'
    #for filename in os.listdir(json_folder_path):
    #    if filename.endswith('.json'):
    #        json_file_path = os.path.join(json_folder_path, filename)
    #        if (os.path.getsize(json_file_path) != 0 and os.path.getsize(
    #                json_file_path) != 68):
    extract_file(json_file_path, param1, param2)
    sorted_graph_nodes = sorted(graphNodes, key=lambda x: x[0])
    filtered_sorted_graph_nodes = []
    printed = 0
    for start_time, globalNodeID, graphEdges, speaker, text in sorted_graph_nodes: # only for testing!! TODO
        if start_time.day == 21 and start_time.month == 5 and start_time.year == 2020:
            filtered_sorted_graph_nodes.append((start_time, globalNodeID, graphEdges, speaker, text))
        elif printed == 0:
            print(f"{start_time.day}.{start_time.month}.{start_time.year}")
            printed = 1

    return filtered_sorted_graph_nodes

def extract_file(json_file_path, param1, param2):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        locutions = data.get("locutions")
        nodes = data.get("nodes")
        edges = data.get("edges")
        node_id_mapping = {}

        # creating a mapping between the actual text ("L") and the paraphrased text ("I") for every node
        for node in nodes:
            if node.get("type") == "I":
                node_id = node.get("nodeID")
                node_id_mapping[node_id] = []
                between_id = None
                # finding the id of the assertion
                for edge in edges:
                    if edge.get("toID") == node_id:
                        for betweenNode in nodes:
                            if betweenNode.get("nodeID") == edge.get("fromID") and betweenNode.get(
                                    "type") == "YA" and betweenNode.get("text") in ["Asserting",
                                                                                    "Rhetorical Questioning",
                                                                                    "Pure Questioning"]:
                                between_id = betweenNode.get("nodeID")
                # finding the id of the corresponding node
                for targetNode in nodes:
                    if targetNode.get("type") == "L":
                        for edge in edges:
                            if edge.get("fromID") == targetNode.get("nodeID") and edge.get("toID") == between_id:
                                node_id_mapping[node_id].append(targetNode.get("nodeID"))

        for node in nodes:
            if node.get("type") == "I":
                node_id = node.get("nodeID")
                message = node.get("text")
                text = None
                start_time = None
                speaker = None
                if node_id_mapping[node_id]:
                    global_node_id = node_id_mapping[node_id][0]
                else:
                    global_node_id = 0

                outgoing_edges = {}
                connection_ids = {

                }
                graph_edges = {}

                for edge in edges:
                    # find the outgoing connections of this node. There are two types:
                    # (1) connections to other "I" nodes and (2) connections to "L" nodes
                    if edge.get("fromID") == node_id:
                        for betweenNode in nodes:
                            if betweenNode.get("nodeID") == edge.get("toID"):
                                if betweenNode.get("type") not in outgoing_edges:
                                    outgoing_edges[betweenNode.get("type")] = []
                                outgoing_edges[betweenNode.get("type")].append(betweenNode.get("nodeID"))
                    if edge.get("fromID") == global_node_id:
                        for betweenNode in nodes:
                            if betweenNode.get("nodeID") == edge.get("toID") and betweenNode.get("type") == "TA":
                                if betweenNode.get("type") not in outgoing_edges:
                                    outgoing_edges[betweenNode.get("type")] = []
                                outgoing_edges[betweenNode.get("type")].append(betweenNode.get("nodeID"))

                # find the corresponding nodes to the outgoing edges
                for targetNode in nodes:
                    if targetNode.get("type") == "I":
                        for edge in edges:
                            for connType in outgoing_edges:
                                if edge.get("fromID") in outgoing_edges[connType] and edge.get(
                                        "toID") == targetNode.get("nodeID"):
                                    if connType not in connection_ids:
                                        connection_ids[connType] = []
                                    connection_ids[connType].append(
                                        (targetNode.get("nodeID"), edge.get("fromID")))

                    elif targetNode.get("nodeID") == global_node_id:
                        text = targetNode.get("text")
                    elif targetNode.get("type") == "L":
                        for edge in edges:

                            if "TA" in outgoing_edges and edge.get("fromID") in outgoing_edges["TA"] and edge.get(
                                    "toID") == targetNode.get("nodeID"):
                                if "TA" not in graph_edges:
                                    graph_edges["TA"] = []
                                graph_edges["TA"].append(targetNode.get("nodeID"))

                    elif targetNode.get("type") == "YA":
                        for edge in edges:

                            for connType, conn in connection_ids.items():
                                for c in conn:
                                    if edge.get("toID") in c[1] and edge.get("fromID") == targetNode.get("nodeID"):
                                        if c[1] == edge.get("toID"):
                                            if connType not in graph_edges:
                                                graph_edges[connType] = []
                                            graph_edges[connType].append(
                                                (node_id_mapping[c[0]], targetNode.get("text")))

                # find the speaker and the start time
                for locution in locutions:
                    if locution.get("nodeID") == global_node_id:
                        if (locution.get("start")) is not None:
                            start_time = datetime.strptime(locution.get("start"), '%Y-%m-%d %H:%M:%S')
                        speaker = locution.get("personID")
                if start_time is None:
                    start_time = datetime.strptime("2025-05-28 19:08:43", '%Y-%m-%d %H:%M:%S')  # just for now
                if global_node_id:
                    graphNodes.append((start_time, global_node_id, graph_edges, speaker, text))
