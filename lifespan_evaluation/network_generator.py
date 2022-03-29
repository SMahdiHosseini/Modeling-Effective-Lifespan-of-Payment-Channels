import networkx as nx
import numpy as np

def write_nodes_to_csv():
    f = open("nodes_temp.csv", "w+")
    f.write("id\n")
    for node in G:
        f.write(str(node) + "\n")

def write_channels_to_csv():
    f = open("channels_temp.csv", "w+")
    f.write("id,edge1_id,edge2_id,node1_id,node2_id,capacity\n")
    for u,v,a in G.edges(data=True):
        # f.write(G[node])
        print(",".join(a.values))

def set_attributes():
    last_chennal_id = 0
    for u,v,a in G.edges(data=True):
        a["id"] = last_chennal_id
        a["edge1_id"] = 2 * last_chennal_id
        a["edge2_id"] = 2 * last_chennal_id + 1
        a["node1_id"] = u
        a["node2_id"] = v
        a["capacity"] = np.random.normal(average_capacity, 0.2, 1)[0]
        last_chennal_id += 1


# number of nodes = 100
# number of channels = 1000
# 
number_of_nodes = 100
average_capacity = 100
G = nx.gnp_random_graph(number_of_nodes, 0.1)

set_attributes()
write_nodes_to_csv()
write_channels_to_csv()




print(G)
