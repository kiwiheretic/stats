import shapefile
import pandas as pd
from mapdrawer import MapDrawer




df = pd.read_csv("DPE389701_population-by-region.csv", skiprows=1)
df.rename(columns={'Unnamed: 0':'Date'}, inplace=True)
regidx = [1,2,3,4,5,6,7,8,9, 13,14,15,16,11,0,12,0] 
nztot = 1569900.0 #df.iloc[19,19].astype(float)

shp_folder = "C:/Users/Glenn/Documents/Stats/ShapeFiles/"
shpf = shapefile.Reader(shp_folder + "REGC2016_GV_Full.shp")
#shp_folder = "C:/Users/Glenn/Documents/Stats/2016 Digital Boundaries Generalised Clipped/"
#shpf = shapefile.Reader(shp_folder + "REGC2016_GV_Clipped.shp")
fields = shpf.fields
for name in fields:
    print name

records = shpf.records()
geom = shpf.shapes()
shades = []
polygons = []
bboxes = []
for fidx, feature in enumerate(geom):
    try:
        if regidx[fidx] == 0: continue
        v = df.iloc[19, regidx[fidx]]
        shades.append(v)
    except IndexError:
        continue
    polygons.append(feature.points)
    bboxes.append(feature.bbox)

map1 = MapDrawer()
img = map1.draw(polygons, shades, bboxes=bboxes, title="Population Distribution of NZ (2015)", legend_header="(million)")
#img = map1.draw(polygons, shades, bboxes=bboxes, legend_header="(million)")
img.save("nz1.png", "PNG")
