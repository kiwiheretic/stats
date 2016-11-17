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

shp_folder = "C:/Users/Glenn/Documents/Stats/2016 Digital Boundaries Generalised Clipped/"
shp_iter = ShapeFileIterator( shp_folder + "REGC2016_GV_Clipped.shp")
shades = permute_values(regidx, df.loc['2016-10-01'])
print shades
map1 = MapDrawer(dimensions=(475,480))
img = map1.draw(shp_iter, shades, title="Bonds Lodged (Oct 2016)", legend_header="(Qty)", exclude_regions=[17], colour_profile=((255,0,0),(0,255,0)))
img.save("bonds-lodged.png", "PNG")
