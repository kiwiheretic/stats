import shapefile

sf = shapefile.Reader(r"C:\Users\Glenn\Documents\Stats\ShapeFiles\TA2016_GV_Full.shp")
shapes = sf.shapes()
print len(shapes)
import pdb; pdb.set_trace()
