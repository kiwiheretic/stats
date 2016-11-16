from datautils import permute_values
import shapefile
import pandas as pd
from mapdrawer import MapDrawer, ShapeFileIterator


#df = pd.read_csv("DPE389701_population-by-region.csv", skiprows=1)
#df.rename(columns={'Unnamed: 0':'Date'}, inplace=True)
regidx = [2,4,11,5,6,8,16, 0,  14, 1, 12, 13, 7, 0, 3, 9, 10] 
stats_folder = "C:/Users/Glenn/Documents/Stats/Housing/"
df = pd.read_csv(stats_folder + "Mean Rents by region.csv", skiprows=0)

shp_folder = "C:/Users/Glenn/Documents/Stats/2016 Digital Boundaries Generalised Clipped/"
shp_iter = ShapeFileIterator( shp_folder + "REGC2016_GV_Clipped.shp")
shades = permute_values(regidx, df.iloc[285, 1:])
print shades
map1 = MapDrawer()
img = map1.draw(shp_iter, shades, title="Median Housing Rental (Oct 2016)", legend_header="($)")
img.save("house-rental-prices.png", "PNG")
