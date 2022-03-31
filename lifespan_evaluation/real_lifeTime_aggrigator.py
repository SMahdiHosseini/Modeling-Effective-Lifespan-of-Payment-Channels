from math import sqrt
from re import I, S
import sys
import pandas as pd
from os import walk
import numpy as np

channels_path = sys.argv[1]
number_of_channels = int(sys.argv[2])
number_of_folders = int(sys.argv[3])

unbalancing_times_matrix = [[] for i in range(number_of_channels)]

for i in range(number_of_folders):
    filenames = next(walk(channels_path + "_" + str(i)), (None, None, []))[2]  # [] if no file
    # filenames.sort()
    print(len(filenames))

    for file in filenames:
        df = pd.read_csv(channels_path + "_" + str(i) + "/" + file)
        # print(file)
        for id in range(number_of_channels):
            unbalancing_time = df[df['id'] == id]['unbalancing_time'].iloc[0] / 1000.
            if unbalancing_time != 0:
                unbalancing_times_matrix[id].append(unbalancing_time)
    
    
f = open("lifeTimes_real.csv", "w+")
f.write("channel_id,life_time,error\n")
for id in range(number_of_channels):
    # print(count_ub[id])
    if len(unbalancing_times_matrix[id]) <= 100:
        f.write(",".join([str(id), str(-1)]) + "\n")
        print("******************************************************")
        continue
    f.write(",".join([str(id), str(np.average(unbalancing_times_matrix[id])), 
    str(sqrt(np.var(unbalancing_times_matrix[id]) / len(unbalancing_times_matrix[id])))]) + "\n")