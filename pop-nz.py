import shapefile
import pandas as pd
from mapdrawer import MapDrawer, ShapeFileIterator




df = pd.read_csv("DPE389701_population-by-region.csv", skiprows=1)
df.rename(columns={'Unnamed: 0':'Date'}, inplace=True)
regidx = [1,2,3,4,5,6,7,8,9, 13,14,15,16,11,0,12,0] 
nztot = 1569900.0 #df.iloc[19,19].astype(float)

#shp_folder = "C:/Users/Glenn/Documents/Stats/ShapeFiles/"
#shpf = shapefile.Reader(shp_folder + "REGC2016_GV_Full.shp")
shp_folder = "C:/Users/Glenn/Documents/Stats/2016 Digital Boundaries Generalised Clipped/"
shp_iter = ShapeFileIterator( shp_folder + "REGC2016_GV_Clipped.shp")

shades = []
for idx in range(0, len(regidx)):
    if regidx[idx] == 0: 
        v = 0
    else:
        v = df.iloc[19, regidx[idx]]
    shades.append(v)

map1 = MapDrawer()
img = map1.draw(shp_iter, shades, title="Population Distribution of NZ (2015)", legend_header="(million)")
#map1.number_regions()
#img = map1.draw(polygons, shades, bboxes=bboxes, legend_header="(million)")
img.save("nz-pop.png", "PNG")
