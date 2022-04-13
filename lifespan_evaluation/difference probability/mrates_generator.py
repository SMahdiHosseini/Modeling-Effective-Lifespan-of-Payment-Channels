from ntpath import join
import sys
import numpy as np

seed = int(sys.argv[1])
number_of_nodes = int(sys.argv[2])
sparse_coef = float(sys.argv[3])
average_rate = float(sys.argv[4]) # in second
std_rate = float(sys.argv[5]) # in second
number_of_pairs = int(((number_of_nodes ** 2) - number_of_nodes) * sparse_coef)

MRates = [[-1 for i in range(number_of_nodes)] for j in range(number_of_nodes)]

for i in range(number_of_pairs):
    x, y = np.random.choice(range(number_of_nodes), 2, False)
    MRates[x][y] = np.abs(np.random.normal(average_rate, std_rate))
    MRates[y][x] = np.abs(np.random.normal(average_rate, std_rate))


f = open("Mrates.csv", "w+")
for i in range(number_of_nodes):
    for j in range(number_of_nodes):
        if MRates[i][j] == -1:
            MRates[i][j] = 0

    f.write(",".join([str(MRates[i][j]) for j in range(number_of_nodes)]) + "\n")
