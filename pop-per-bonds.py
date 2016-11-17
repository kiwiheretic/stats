from datautils import permute_values
import shapefile
import pandas as pd
from mapdrawer import MapDrawer, ShapeFileIterator


#df = pd.read_csv("DPE389701_population-by-region.csv", skiprows=1)
#df.rename(columns={'Unnamed: 0':'Date'}, inplace=True)
regidx = [2,4,11,5,6,8,16, None,  14, 1, 12, 13, 7, None, 3, 9, 10] 
stats_folder = "C:/Users/Glenn/Documents/Stats/Housing/"
df = pd.read_csv(stats_folder + "Bonds Lodged by region.csv", skiprows=0)
df.set_index('Month', inplace=True)

dfpop = pd.read_csv("DPE389701_population-by-region.csv", skiprows=1, nrows=21)
dfpop.rename(columns={'Unnamed: 0':'Date', 'New Zealand':'Population'}, inplace=True)
dfpop = dfpop.set_index('Date')
dfpop.apply(pd.to_numeric)
popidx = [1,2,3,4,5,6,7,8,9,None,14,16,10,11,12,13,None]
popvalues = permute_values(popidx, dfpop.loc['2015'])

shp_folder = "C:/Users/Glenn/Documents/Stats/2016 Digital Boundaries Generalised Clipped/"
shp_iter = ShapeFileIterator( shp_folder + "REGC2016_GV_Clipped.shp")
bonds = permute_values(regidx, df.loc['2016-10-01'])

popbond = []
for ii in range(17):
    if bonds[ii] and popvalues[ii]:
        x = popvalues[ii] / bonds[ii]
    else:
        x = None
    popbond.append(x)
print popbond 
map1 = MapDrawer(dimensions=(475,480))
img = map1.draw(shp_iter, popbond, title="Population per Bonds Lodged", legend_header="(Pop/Bond Ratio)", exclude_regions=[17], colour_profile=((255,0,0),(0,255,0)))
img.save("pop-lodged-bonds.png", "PNG")
