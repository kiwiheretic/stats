from datautils import permute_values
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# You typically want your plot to be ~1.33x wider than tall. This plot
# is a rare exception because of the number of lines being plotted on it.
# Common sizes: (10, 7.5) and (12, 9)
fig, ax = plt.subplots(1, 1, figsize=(6.5, 7))

# These are the colors that will be used in the plot
color_sequence = ['#1f77b4', '#ff7f0e', '#2ca02c',
                  '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

                  
#df = pd.read_csv("DPE389701_population-by-region.csv", skiprows=1)
#df.rename(columns={'Unnamed: 0':'Date'}, inplace=True)
regidx = [2,4,11,5,6,8,16, None,  14, 1, 12, 13, 7, None, 3, 9, 10] 
stats_folder = "C:/Users/Glenn/Documents/Stats/Housing/"
df = pd.read_csv(stats_folder + "Active Bonds by region.csv", skiprows=0)
df.set_index('Month', inplace=True)
df.rename(pd.to_datetime, inplace=True)
df = df.groupby(df.index.year).mean()
df = df['National Total']

r1 = df.index.values[0]
r2 = df.index.values[-1]

ax = df.plot(title="Rental Housing Growth", grid=True)
lbls = []
for yr in range(r1, r2+1):
    if yr % 5 == 0:
        lbls.append(yr)
    else:
        lbls.append('')
plt.xticks(np.arange(r1,r2+1), lbls)
lbls = []
for yv in np.arange(100000, 410000, 10000):
    if yv % 50000 == 0:
        lbls.append(yv)
    else:
        lbls.append('')
ax.set_xlabel('Year')
ax.set_ylabel('National Active Bonds')
# Stop ylabel from disappearing off edge
plt.subplots_adjust(bottom=.1, left=.2)    

plt.yticks(np.arange(100000, 410000, 10000), lbls)
fig = ax.get_figure()
fig.savefig("national-active-bonds-ts.png")
