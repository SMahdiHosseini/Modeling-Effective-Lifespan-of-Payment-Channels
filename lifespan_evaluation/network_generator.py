from nbformat import write
import networkx as nx
import numpy as np

def write_nodes_to_csv():
    f = open("nodes.csv", "w+")
    f.write("id\n")
    for node in G:
        f.write(str(node) + "\n")

def write_channels_to_csv():
    f = open("channels.csv", "w+")
    f.write("id,edge1_id,edge2_id,node1_id,node2_id,capacity\n")
    for u,v,a in G.edges(data=True):
        f.write(",".join([str(item) for item in a.values()]) + "\n")

def write_edges_to_csv():
    f = open("edges.csv", "w+")
    f.write("id,channel_id,counter_edge_id,from_node_id,to_node_id,balance,fee_base,fee_proportional,min_htlc,timelock\n")

    for u,v,a in G.edges(data=True):
        edge1_data = {}
        edge2_data = {}

        edge1_data["id"] = a["edge1_id"]
        edge2_data["id"] = a["edge2_id"]

        edge1_data["channel_id"] = a["id"]
        edge2_data["channel_id"] = a["id"]

        edge1_data["counter_edge_id"] = a["edge2_id"]
        edge2_data["counter_edge_id"] = a["edge1_id"]

        edge1_data["from_node_id"] = a["node1_id"]
        edge2_data["from_node_id"] = a["node2_id"]

        edge1_data["to_node_id"] = a["node2_id"]
        edge2_data["to_node_id"] = a["node1_id"]

        edge1_data["balance"] = a["capacity"] / 2
        edge2_data["balance"] = a["capacity"] / 2

        edge1_data["fee_base"] = fee_base
        edge2_data["fee_base"] = fee_base

        edge1_data["fee_proportional"] = fee_proportional
        edge2_data["fee_proportional"] = fee_proportional

        edge1_data["min_htlc"] = min_htlc
        edge2_data["min_htlc"] = min_htlc

        edge1_data["timelock"] = timelock
        edge2_data["timelock"] = timelock

        f.write(",".join([str(item) for item in edge1_data.values()]) + "\n")
        f.write(",".join([str(item) for item in edge2_data.values()]) + "\n")

def set_attributes():
    last_chennal_id = 0
    for u,v,a in G.edges(data=True):
        a["id"] = last_chennal_id
        a["edge1_id"] = 2 * last_chennal_id
        a["edge2_id"] = 2 * last_chennal_id + 1
        a["node1_id"] = u
        a["node2_id"] = v
        a["capacity"] = int(np.random.normal(average_capacity, average_capacity / 10, 1)[0])
        last_chennal_id += 1


# number of nodes = 100
# number of channels = 1000
# 
number_of_nodes = 100
average_capacity = 18000000
fee_base = 0
fee_proportional = 0
min_htlc = 100
timelock = 140


G = nx.gnp_random_graph(number_of_nodes, 0.1)

set_attributes()
write_nodes_to_csv()
write_channels_to_csv()
write_edges_to_csv()



print(G)
