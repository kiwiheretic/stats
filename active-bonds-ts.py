from datautils import permute_values
import pandas as pd
import matplotlib.pyplot as plt

# You typically want your plot to be ~1.33x wider than tall. This plot
# is a rare exception because of the number of lines being plotted on it.
# Common sizes: (10, 7.5) and (12, 9)
fig, ax = plt.subplots(1, 1, figsize=(6, 7))

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
del df['National Total']
df = df[['Auckland','Waikato','Wellington','Canterbury','Bay of Plenty']]

# Remove the plot frame lines. They are unnecessary here.
ax.spines['top'].set_visible(False)
#ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
#ax.spines['left'].set_visible(False)

# Ensure that the axis ticks only show up on the bottom and left of the plot.
# Ticks on the right and top of the plot are generally unnecessary.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Provide tick lines across the plot to help your viewers trace along
# the axis ticks. Make sure that the lines are light and small so they
# don't obscure the primary data lines.
r1 = df.index.values[0]
r2 = df.index.values[-1]
for yr in range(r1, r2+1):
    plt.axvline(yr, lw=2, color="black", alpha=0.1)


for y in range(10000, 150000, 10000):
    xmax = 1 - 1.0/(r2-r1)
    plt.axhline(y, xmax=xmax, lw=2, color="black", alpha=0.1)
## Remove the tick marks; they are unnecessary with the tick lines we just
## plotted.
#plt.tick_params(axis='both', which='both', bottom='off', top='off',
#                labelbottom='on', left='off', right='off', labelleft='on')
# remove unnecessary white space
lastx=df.index.values[-1]
plt.xlim(df.index.values[0], lastx+1)
yoffsets = {'Auckland':-5000, 'Canterbury': -8000, 'Waikato': -10000,
            'Bay of Plenty':-8000}
for idx, col in enumerate(df.columns):
    plt.plot(df.index.values, df[col], lw=2, color=color_sequence[idx] )
    y_pos = int(df[col].loc[lastx])
    if col in yoffsets: 
        y_pos += yoffsets[col]
    plt.text(lastx-5, y_pos, df.columns[idx], fontsize=14, color=color_sequence[idx])

plt.title("Active Bonds (5 Regions)")
ax.set_xlabel('Year')
ax.set_ylabel('Bonds Held')
fig.savefig("active-bonds-ts.png")
