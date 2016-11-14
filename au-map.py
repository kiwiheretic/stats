import shapefile
import pandas as pd
from mapdrawer import MapDrawer





#shp_folder = "C:/Users/Glenn/Documents/Stats/ShapeFiles/"
#shpf = shapefile.Reader(shp_folder + "REGC2016_GV_Full.shp")
shp_folder = "C:/Users/Glenn/Documents/Stats/2016 Digital Boundaries Generalised Clipped/"
shpf = shapefile.Reader(shp_folder + "CB2016_GV_Clipped.shp")
fields = shpf.fields
for name in fields:
    print name

records = shpf.records()
geom = shpf.shapes()
shades = []
polygons = []
bboxes = []
for fidx, feature in enumerate(geom):
    parts = []
    for idx in range(len(feature.parts)-1):
        pidx1 = feature.parts[idx]
        pidx2 = feature.parts[idx+1]
        parts.append(feature.points[pidx1:pidx2-1])
    parts.append(feature.points[feature.parts[-1]:])
    polygons.append(parts)
    bboxes.append(feature.bbox)

map1 = MapDrawer()
img = map1.draw(polygons, shades, draw_legend = False, bboxes=bboxes, title="Community Boards")
img.save("community-boards.png", "PNG")
