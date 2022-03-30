from re import I
import sys
import pandas as pd
from os import walk

channels_path = sys.argv[1]
number_of_channels = int(sys.argv[2])
number_of_folders = int(sys.argv[3])

count_ub = [0 for i in range(number_of_channels)]
unbalancing_time_agg = [0 for i in range(number_of_channels)]

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
                unbalancing_time_agg[id] += unbalancing_time
                count_ub[id] += 1
    
    
f = open("lifeTimes_real.csv", "w+")
f.write("channel_id,life_time\n")
for id in range(number_of_channels):
    print(count_ub[id])
    if count_ub[id] <= 100:
        f.write(",".join([str(id), str(-1)]) + "\n")
        # print("******************************************************")
        continue
    f.write(",".join([str(id), str(unbalancing_time_agg[id] / count_ub[id])]) + "\n")