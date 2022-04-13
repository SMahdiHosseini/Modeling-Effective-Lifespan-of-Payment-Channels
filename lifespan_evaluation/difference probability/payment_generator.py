import numpy as np
import sys
import pandas as pd

seed = int(sys.argv[1])
simulation_time = int(sys.argv[2])
MRates_file = str(sys.argv[3])
payment_amount_avg = int(sys.argv[4])
payment_amount_std = int(sys.argv[5])

np.random.seed(seed)

def convert(x):
    try:
        return x.astype(int)
    except:
        return x

# Read MRates and save
Mrates = {}
file = open(MRates_file)
lines = file.readlines()
for i in range(len(lines)):
    line = [float(k) for k in lines[i].split(',')]
    for j in range(len(line)):
        # if line[j] != 0:
        Mrates[(i, j)] = line[j]

# Generate Payments
## Create Empty dataframe
payments_df = pd.DataFrame(columns=['sender_id','receiver_id','amount','start_time'])
# id = 0
for key in Mrates.keys():
    payment_time = 0
    if Mrates[key] != 0:
        while payment_time <= simulation_time * 1000:
            payment_time += np.random.poisson(1 / Mrates[key] * 1000) # pyaments times in millisecond
            # id += 1
            payments_df.loc[len(payments_df.index)] =  [int(key[0]), int(key[1]), np.random.normal(payment_amount_avg, payment_amount_std), payment_time]

payments_df = payments_df.sort_values('start_time', ignore_index=True)
payments_df.index.name = 'id'
# print(payments_df.apply(convert).info())
payments_df.apply(convert).to_csv("payments.csv", index=True)
    
