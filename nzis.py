import shapefile
import pandas as pd
from mapdrawer import MapDrawer, ShapeFileIterator
from datautils import permute_values

regions = [1,2,3,4,[5,6],7,8,9,[14,15,16,10],11,12,13] 

stats_folder = "C:/Users/Glenn/Documents/Stats/Housing/"
df = pd.read_csv("nzis-jun2015qtr-regional.csv", skiprows=10, names=['Region','Unused', '2011', '2012', '2013', '2014', '2015'],nrows=13).drop('Unused', axis=1)


shp_folder = "C:/Users/Glenn/Documents/Stats/2016 Digital Boundaries Generalised Clipped/"
shp_iter = ShapeFileIterator( shp_folder + "REGC2016_GV_Clipped.shp")

shades = permute_values(regions, df['2015'])
print shades


map1 = MapDrawer(dimensions=(475,480))
img = map1.draw(shp_iter, shades, title="Median Income (June 2015)", legend_header="($)", exclude_regions=[17])
img.save("income-regional.png", "PNG")
