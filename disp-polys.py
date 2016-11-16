import shapefile
import pandas as pd
from mapdrawer import MapDrawer


#shp_folder = "C:/Users/Glenn/Documents/Stats/ShapeFiles/"
#shpf = shapefile.Reader(shp_folder + "REGC2016_GV_Full.shp")
shp_folder = "C:/Users/Glenn/Documents/Stats/2016 Digital Boundaries Generalised Clipped/"
shpf = shapefile.Reader(shp_folder + "REGC2016_GV_Clipped.shp")
fields = shpf.fields
for name in fields:
    print name

records = shpf.records()
geom = shpf.shapes()
shades = []
polygons = []
bboxes = []
for fidx, feature in enumerate(geom):
    cnt = sx = sy = 0
    for x,y in feature.points:
        sx += x
        sy += y
        cnt += 1
    print (sx/cnt, sy/cnt)

map = MapDrawer()
map.draw(polygons)


