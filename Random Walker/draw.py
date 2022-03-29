import pandas as pd
import matplotlib.pyplot as plt


failRate = [[0.40210848457252746, 0.29816719860597757, 0.2016757416235182, 0.09589101782297213, 0.05370414286815328], 
        [0.39571251914637984, 0.3066264485792061, 0.20204162857098518, 0.10157534777508544, 0.030612392489829592], 
        [0.4130493829538149, 0.31384428222885796, 0.2018470889908774, 0.09852556859736283, 0.024031980539353577], 
        [0.392779352582707, 0.2996850877047831, 0.20035109205024892, 0.10718582831447143, 0.020948429273389677], 
        [0.3927682935664669, 0.2857999883984695, 0.19231826954871603, 0.09831346098572068, 0.023301757362559357]]

cap = [10, 15, 20, 25, 30]
prob = [0.3, 0.35, 0.4, 0.45, 0.5]
data = []

for c in range(5):
    for p in range(5):
        data.append([cap[c], prob[p], failRate[c][p]])
        
dataFrame = pd.DataFrame(data, columns=['capacity', 'probability', 'failRate'])

f = plt.figure(figsize=(19, 15))
plt.matshow(dataFrame.corr(), fignum=f.number)
# plt.xticks(range(dataFrame.select_dtypes(['capacity']).shape[1]), dataFrame.select_dtypes(['capacity']).columns, fontsize=14, rotation=45)
# plt.yticks(range(dataFrame.select_dtypes(['capacity']).shape[1]), dataFrame.select_dtypes(['capacity']).columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
plt.title('Correlation Matrix', fontsize=16);
plt.matshow(dataFrame.corr())
plt.show()