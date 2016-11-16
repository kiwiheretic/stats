from datautils import permute_values
import shapefile
import pandas as pd
from mapdrawer import MapDrawer, ShapeFileIterator


#df = pd.read_csv("DPE389701_population-by-region.csv", skiprows=1)
#df.rename(columns={'Unnamed: 0':'Date'}, inplace=True)
rental_regions = [2,4,11,5,6,8,16, None,  14, 1, 12, 13, 7, None, 3, 9, 10] 
stats_folder = "C:/Users/Glenn/Documents/Stats/Housing/"
df_rents = pd.read_csv(stats_folder + "Mean Rents by region.csv", skiprows=0)

income_regions = [1,2,3,4,[5,6],7,8,9,[14,15,16,10],11,12,13] 
stats_folder = "C:/Users/Glenn/Documents/Stats/Housing/"
df_income = pd.read_csv("nzis-jun2015qtr-regional.csv", skiprows=10, names=['Region','Unused', '2011', '2012', '2013', '2014', '2015'],nrows=13).drop('Unused', axis=1)


shp_folder = "C:/Users/Glenn/Documents/Stats/2016 Digital Boundaries Generalised Clipped/"
shp_iter = ShapeFileIterator( shp_folder + "REGC2016_GV_Clipped.shp")

rentals = permute_values(rental_regions, df_rents.iloc[285, 1:] )
income = permute_values(income_regions, df_income['2015'])
shades = []
for ii in range(0,len(rentals)):
    if income[ii] == None or rentals[ii] == None:
        shades.append(None)
    else:
        shades.append(income[ii] - (rentals[ii]))
print income
print rentals
print shades
map1 = MapDrawer(dimensions=(475, 480))
img = map1.draw(shp_iter, shades, title="Median Income After Rent", legend_header="($)", use_divisor=False, exclude_regions = [17], colour_profile=((0,255,0),(255,0,0)))
img.save("income-after-rent.png", "PNG")
