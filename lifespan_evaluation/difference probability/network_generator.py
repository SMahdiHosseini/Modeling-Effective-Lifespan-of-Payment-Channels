from textwrap import shorten
from nbformat import write
import networkx as nx
import numpy as np
import lamba_calculator as lm
import sys
import networkx as nx
import numpy as np



def write_nodes_to_csv():
    f = open("nodes.csv", "w+")
    f.write("id\n")
    for node in H:
        f.write(str(node) + "\n")

def write_channels_to_csv():
    f = open("channels.csv", "w+")
    f.write("id,edge1_id,edge2_id,node1_id,node2_id,capacity\n")
    for u,v,a in H.edges(data=True):
        f.write(",".join([str(item) for item in a.values()]) + "\n")

def write_edges_to_csv():
    f = open("edges.csv", "w+")
    f.write("id,channel_id,counter_edge_id,from_node_id,to_node_id,balance,fee_base,fee_proportional,min_htlc,timelock\n")

    for u,v,a in H.edges(data=True):
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

        edge1_data["balance"] = int(a["capacity"] / 2)
        edge2_data["balance"] = int(a["capacity"] / 2)

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
    for u,v,a in H.edges(data=True):
        a["id"] = last_chennal_id
        a["edge1_id"] = 2 * last_chennal_id
        a["edge2_id"] = 2 * last_chennal_id + 1
        a["node1_id"] = u
        a["node2_id"] = v
        a["capacity"] = int(np.random.normal(average_capacity, average_capacity / 10, 1)[0])
        last_chennal_id += 1

def write_expected_lifetimes():
    f = open("lifeTimes.csv", "w+")
    f.write("channel_id,life_time\n")
    

    for u,v,at in H.edges(data=True):
        p = lambdas[(u, v)] / (lambdas[(u, v)] + lambdas[(v, u)])
        q = lambdas[(v, u)] / (lambdas[(u, v)] + lambdas[(v, u)])
        a = (at["capacity"] / average_payment_amount) / 2
        b = (at["capacity"] / average_payment_amount) / 2
        rate = (lambdas[(u, v)] + lambdas[(v, u)])
        if p == q:
            expected_steps = a * b
        else:
            expected_steps = ((a * (p ** a) * ((p ** b) - (q ** b))) + (b * (q ** b) * ((q ** a) - (p ** a)))) / ((p - q) * ((p ** (a + b)) - (q ** (a + b))))

        expected_life_time = expected_steps / rate
        f.write(",".join([str(at["id"]), str(expected_life_time)]) + "\n")

def edge_included_shortest_path(shortest_paths, u, v):
    number_of_paths = 0
    for path in shortest_paths:
        for i in range(len(path) - 1):
            if path[i] == u and path[i + 1] == v:
                number_of_paths += 1
                break
    return number_of_paths
    
def calc_lambdas(all_shortest_paths):
    lambdas = {}
    for u, v, a in G.edges(data=True):
        lambdas[(u, v)] = 0
        for s in G.nodes:
            for t in G.nodes:
                if s == t:
                    continue
                lambdas[(u, v)] += edge_included_shortest_path(all_shortest_paths[(s, t)], u, v) / len(all_shortest_paths[(s, t)]) * Mrates[(s, t)]
    return lambdas

def all_shortest_paths():
    shortest_paths = {}
    for u in G.nodes:
        for v in G.nodes:
            if u == v:
                continue
            shortest_paths[(u, v)] = [p for p in nx.all_shortest_paths(G, source=u, target=v)]
    return shortest_paths



seed = int(sys.argv[1])
number_of_nodes = int(sys.argv[2])
channel_existance_prob = float(sys.argv[3])
average_capacity = int(sys.argv[4])
average_payment_amount = int(sys.argv[5]) *1000
MRates_file = str(sys.argv[6])
fee_base = int(sys.argv[7])
fee_proportional = int(sys.argv[8])
min_htlc = int(sys.argv[9])
timelock = int(sys.argv[10])

# Read MRates and save
Mrates = {}
file = open(MRates_file)
lines = file.readlines()
for i in range(len(lines)):
    line = [float(k) for k in lines[i].split(',')]
    for j in range(len(line)):
        # if line[j] != 0:
        Mrates[(i, j)] = line[j]


H = nx.gnp_random_graph(number_of_nodes, channel_existance_prob, seed=seed)
G = nx.DiGraph()
for u,v,a in H.edges(data=True):
    G.add_edge(u, v)
    G.add_edge(v, u)


set_attributes()
write_nodes_to_csv()
write_channels_to_csv()
write_edges_to_csv()

all_shortest_paths_ = all_shortest_paths()
lambdas = calc_lambdas(all_shortest_paths_)

write_expected_lifetimes()

print(len(H.edges(data=True)))
