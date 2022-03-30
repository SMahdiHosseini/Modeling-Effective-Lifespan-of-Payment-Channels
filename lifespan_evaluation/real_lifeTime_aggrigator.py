from re import I
import sys
import pandas as pd
from os import walk

channels_path = sys.argv[1]
number_of_channels = int(sys.argv[2])

filenames = next(walk(channels_path), (None, None, []))[2]  # [] if no file

count_ub = [0 for i in range(number_of_channels)]
unbalancing_time_agg = [0 for i in range(number_of_channels)]

for file in filenames:
    df = pd.read_csv(channels_path + file)
    print(file)
    for id in range(number_of_channels):
        unbalancing_time = df[df['id'] == id]['unbalancing_time'].iloc[0] / 1000
        if unbalancing_time != 0:
            unbalancing_time_agg[id] += unbalancing_time
            count_ub[id] += 1
    
    
f = open("lifeTimes_real.csv", "w+")
f.write("channel_id,life_time\n")
for id in range(number_of_channels):
    f.write(",".join([str(id), str(unbalancing_time_agg[id] / count_ub[id])]) + "\n")