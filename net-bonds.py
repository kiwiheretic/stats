from datautils import permute_values
import shapefile
import pandas as pd
from mapdrawer import MapDrawer, ShapeFileIterator


regidx = [2,4,11,5,6,8,16, None,  14, 1, 12, 13, 7, None, 3, 9, 10] 
stats_folder = "C:/Users/Glenn/Documents/Stats/Housing/"
dfopen = pd.read_csv(stats_folder + "Bonds Lodged by region.csv", skiprows=0)
dfopen.set_index('Month', inplace=True)
dfclose = pd.read_csv(stats_folder + "Bonds Closed by region.csv", skiprows=0)
dfclose.set_index('Month', inplace=True)
df = dfopen.subtract(dfclose)

shp_folder = "C:/Users/Glenn/Documents/Stats/2016 Digital Boundaries Generalised Clipped/"
shp_iter = ShapeFileIterator( shp_folder + "REGC2016_GV_Clipped.shp")
shades = permute_values(regidx, df.loc['2016-10-01'])
print shades
map1 = MapDrawer(dimensions=(475,480))
img = map1.draw(shp_iter, shades, title="Net Bonds Lodged (Oct 2016)", legend_header="(Qty)", exclude_regions=[17], colour_profile=((255,0,0),(0,255,0)))
img.save("net-bonds-lodged.png", "PNG")
