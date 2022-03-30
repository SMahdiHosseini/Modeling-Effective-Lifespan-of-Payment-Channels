import sys
import pandas as pd
from os import walk

channels_path = sys.argv[1]

filenames = next(walk(channels_path), (None, None, []))[2]  # [] if no file

count_ub = 0
unbalancing_time_agg = 0

for file in filenames:
    df = pd.read_csv(channels_path + file)
    unbalancing_time = df[df['id'] == 0]['unbalancing_time'].iloc[0]
    if unbalancing_time != 0:
        unbalancing_time_agg += unbalancing_time
        count_ub += 1
        
print(unbalancing_time_agg / count_ub)