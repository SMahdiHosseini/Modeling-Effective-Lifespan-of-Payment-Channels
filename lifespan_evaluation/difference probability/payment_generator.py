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

def generate_payment(Mrate_keys, tid):
    for key in Mrate_keys:
        payment_time = 0
        if Mrates[key] != 0:
            while payment_time <= simulation_time * 1000:
                payment_time += np.random.exponential(1 / Mrates[key] * 1000) # pyaments times in millisecond
                payments_df[tid].loc[len(payments_df[tid].index)] =  [int(key[0]), int(key[1]), np.random.normal(payment_amount_avg, payment_amount_std) * 1000, payment_time]


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
payments_df = [pd.DataFrame(columns=['sender_id','receiver_id','amount','start_time']) for i in range(processCount)]
keys = [key for key in Mrates.keys()]

p0 = multiprocessing.Process(target=generate_payment, args=(keys[0::4], 0))
p1 = multiprocessing.Process(target=generate_payment, args=(keys[1::4], 1))
p2 = multiprocessing.Process(target=generate_payment, args=(keys[2::4], 2))
p3 = multiprocessing.Process(target=generate_payment, args=(keys[3::4], 3))

p0.start()
p1.start()
p2.start()
p3.start()

p0.join()
p1.join()
p2.join()
p3.join()

all_payments_df = pd.concat(payments_df)


all_payments_df = all_payments_df.sort_values('start_time', ignore_index=True)
all_payments_df.index.name = 'id'
# print(payments_df.apply(convert).info())
all_payments_df.apply(convert).to_csv("payments.csv", index=True)
    
