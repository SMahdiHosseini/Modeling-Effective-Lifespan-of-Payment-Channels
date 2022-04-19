import numpy as np
import sys
import pandas as pd
import multiprocessing

processCount = 4

seed = int(sys.argv[1])
simulation_time = int(sys.argv[2])
MRates_file = str(sys.argv[3])
payment_amount_avg = int(sys.argv[4])
payment_amount_std = int(sys.argv[5])

np.random.seed(seed)


payments_df = [pd.DataFrame(columns=['sender_id','receiver_id','amount','start_time']) for i in range(processCount)]
# Read MRates and save
Mrates = {}
file = open(MRates_file)
lines = file.readlines()
for i in range(len(lines)):
    line = [float(k) for k in lines[i].split(',')]
    for j in range(len(line)):
        # if line[j] != 0:
        Mrates[(i, j)] = line[j]

def generate_payment(Mrate_keys, tid, return_dict):
    for key in Mrate_keys:
        payment_time = 0
        if Mrates[key] != 0:
            while payment_time <= simulation_time * 1000:
                payment_time += np.random.exponential(1 / Mrates[key] * 1000) # pyaments times in millisecond
                payments_df[tid].loc[len(payments_df[tid].index)] =  [int(key[0]), int(key[1]), np.random.normal(payment_amount_avg, payment_amount_std) * 1000, payment_time]
    return_dict[procnum] = payments_df[procnum]
    # print(payments_df[tid].info())

def convert(x):
    try:
        return x.astype(int)
    except:
        return x


# Generate Payments
## Create Empty dataframe
keys = [key for key in Mrates.keys()]

manager = multiprocessing.Manager()
return_dict = manager.dict()

jobs = []

for procnum in range(processCount):
    proc = multiprocessing.Process(target=generate_payment, args=(keys[procnum::4], procnum, return_dict))
    jobs.append(proc)
    proc.start()

for proc in jobs:
    proc.join()



all_payments_df = return_dict[0]
all_payments_df = all_payments_df.append(return_dict[1])
all_payments_df = all_payments_df.append(return_dict[2])
all_payments_df = all_payments_df.append(return_dict[3])

# print(return_dict[0].info())
# print(return_dict[1].info())
# print(return_dict[2].info())
# print(return_dict[3].info())
# print(all_payments_df.info())

all_payments_df = all_payments_df.sort_values('start_time', ignore_index=True)
all_payments_df.index.name = 'id'
# print(payments_df.apply(convert).info())
all_payments_df.apply(convert).to_csv("payments.csv", index=True)
    
