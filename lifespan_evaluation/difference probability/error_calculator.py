import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import scipy as sp
from scipy import stats

real_df = pd.read_csv("lifeTimes_real.csv")
prediction_df = pd.read_csv("lifeTimes.csv")
real = []
pred = []
p_values = []
t = []
for index, row in real_df.iterrows():
    real_life_time = row['life_time']
    real_life_time_error = row['error']
    predicted_life_time = prediction_df.iloc[index]['life_time']
    if real_life_time == -1:
        continue
    real.append(real_life_time)
    pred.append(predicted_life_time)
    p_values.append(stats.t.sf(np.abs(((real_life_time - predicted_life_time) / real_life_time_error)), row['count'] - 1) * 2)
    t.append(np.abs(((real_life_time - predicted_life_time) / real_life_time_error)))

print(f"p value :{np.average(p_values)}")

error_agg = 0
error_count = 0
errors = []
real = []
pred = []
for index, row in real_df.iterrows():
    real_life_time = row['life_time']
    predicted_life_time = prediction_df.iloc[index]['life_time']
    if real_life_time == -1:
        continue
    real.append(real_life_time)
    pred.append(predicted_life_time)
    error_agg += np.abs(real_life_time - predicted_life_time) / real_life_time
    errors.append(np.abs(real_life_time - predicted_life_time) / real_life_time)
    error_count += 1


print(f"total error: {error_agg / error_count}")
pred_median = np.median(pred)
real_median = np.median(real)

error_agg = 0
error_count = 0
errors = []
real = []
pred = []
for index, row in real_df.iterrows():
    real_life_time = row['life_time']
    predicted_life_time = prediction_df.iloc[index]['life_time']
    if real_life_time == -1 or real_life_time > real_median:
        continue
    real.append(real_life_time)
    pred.append(predicted_life_time)
    error_agg += np.abs(real_life_time - predicted_life_time) / real_life_time
    errors.append(np.abs(real_life_time - predicted_life_time) / real_life_time)
    error_count += 1

print(f"first half of real: {error_agg / error_count}")

error_agg = 0
error_count = 0
errors = []
real = []
pred = []
for index, row in real_df.iterrows():
    real_life_time = row['life_time']
    predicted_life_time = prediction_df.iloc[index]['life_time']
    if real_life_time == -1 or predicted_life_time > pred_median:
        continue
    real.append(real_life_time)
    pred.append(predicted_life_time)
    error_agg += np.abs(real_life_time - predicted_life_time) / real_life_time
    errors.append(np.abs(real_life_time - predicted_life_time) / real_life_time)
    error_count += 1

print(f"first half of pred: {error_agg / error_count}")