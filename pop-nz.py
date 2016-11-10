from PIL import Image, ImageDraw, ImageFont
import shapefile
import math
import pandas as pd

df = pd.read_csv("DPE389701_population-by-region.csv", skiprows=1)
df.rename(columns={'Unnamed: 0':'Date'}, inplace=True)
regidx = [1,2,3,4,5,6,7,8,9, 13,14,15,16,11,0,12] 
nztot = 1569900.0 #df.iloc[19,19].astype(float)

shp_folder = "C:/Users/Glenn/Documents/Stats/ShapeFiles/"
shpf = shapefile.Reader(shp_folder + "REGC2016_GV_Full.shp")
fields = shpf.fields
for name in fields:
    print name

records = shpf.records()

def conv_coord(x,y, rot=15):
    minx, miny, maxx, maxy = 1000000, 4500000, 2600000, 6300000
    ctrx = (maxx+minx)/2
    ctry = (maxy+miny)/2
    rad = rot*math.pi/180
    rx = math.cos(rad)*(x-ctrx)-math.sin(rad)*(y-ctry)
    ry = math.sin(rad)*(x-ctrx)+math.cos(rad)*(y-ctry)
    scr_width, scr_height = 640, 480
    newx = int(float(ctrx+rx-minx)/(maxx-minx)*scr_width)
    newy = scr_height - int(float(ctry+ry-miny)/(maxy-miny)*scr_height)
    return (newx, newy)

im = Image.new('RGB', (640, 480), color="white")
draw = ImageDraw.Draw(im)
font = ImageFont.truetype("arial.ttf", 15)


geom = shpf.shapes()
for fidx, feature in enumerate(geom):
    x1,y1,x2,y2 = feature.bbox
    xs1,ys1 = conv_coord(x1,y1)
    xs2,ys2 = conv_coord(x2,y2)
    if len(feature.parts) > 1:
        continue
    if regidx[fidx] == 0: continue
    #print (x1,y2,x2,y2)
    #print (xs1, ys1, xs2, ys2)
    # create empty list to store all the coordinates
    poly_list = []
    slices = []
    feature_div = 0
    for idx, feature_div in enumerate(feature.parts[1:]):
        slices.append(feature.points[feature.parts[idx]:feature_div])
    slices.append(feature.points[feature_div:])
    lastx, lasty = None, None
    # get each coord that makes up the polygon
    for points_slice in slices:
        for coords in points_slice:
           x, y = conv_coord(coords[0], coords[1])
           if lastx != x or lasty != y:
               poly_coord = (x, y)
               # append the coords to the polygon list
               poly_list.append(poly_coord)
           lastx, lasty = x,y    
        #print df.iloc[19, regidx[fidx]]
        greyness = 255-int(df.iloc[19, regidx[fidx]].astype(float)*200/nztot)
        print greyness
        draw.polygon(poly_list, outline="blue", fill=(greyness,greyness,greyness))
        xm = (xs1+xs2)/2
        ym = (ys1+ys2)/2
        #draw.text((xm, ym), str(fidx+1), font=font, fill="black")


#print poly_list


del draw
im.save("nz1.png", "PNG")
