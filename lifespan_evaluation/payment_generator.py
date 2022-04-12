import numpy as np
import sys
import pandas as pd

seed = int(sys.argv[1])
simulation_time = int(sys.argv[2])
MRates_file = str(sys.argv[3])
payment_amount = int(sys.argv[4])

# Read MRates and save
Mrates = {}
file = open(MRates_file)
lines = file.readlines()
for i in range(len(lines)):
    line = [int(i) for i in lines[i].split(',')]
    for j in range(len(line)):
        if line[j] != 0:
            Mrates[(i, j)] = line[j]

# Generate Payments
## Create Empty dataframe
payments_df = pd.DataFrame(columns=['sender_id','receiver_id','amount','start_time'])
# id = 0
for key in Mrates.keys():
    payment_time = 0
    while payment_time <= simulation_time * 1000:
        payment_time += np.random.poisson(1 / Mrates[key] * 1000) # pyaments times in millisecond
        # id += 1
        payments_df.loc[len(payments_df.index)] =  [key[0], key[1], payment_amount, payment_time]

payments_df = payments_df.sort_values('start_time', ignore_index=True)
payments_df.index.name = 'id'
payments_df.to_csv("payments.csv", index=True)
    
