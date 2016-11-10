from PIL import Image, ImageDraw, ImageFont
import shapefile
import math
import pandas as pd

df = pd.read_csv("DPE389701_population-by-region.csv", skiprows=1)
df.rename(columns={'Unnamed: 0':'Date'}, inplace=True)
regidx = [1,2,3,4,5,6,7,8,9, 13,14,15,16,11,0,12] 
nztot = 1569900.0 #df.iloc[19,19].astype(float)
mingrey=20
maxgrey=170

shp_folder = "C:/Users/Glenn/Documents/Stats/ShapeFiles/"
shpf = shapefile.Reader(shp_folder + "REGC2016_GV_Full.shp")
fields = shpf.fields
for name in fields:
    print name

records = shpf.records()

scr_width, scr_height = 540, 480
def conv_coord(x,y, rot=10):
    minx, miny, maxx, maxy = 1000000, 4500000, 2600000, 6300000
    ctrx = (maxx+minx)/2
    ctry = (maxy+miny)/2
    rad = rot*math.pi/180
    rx = math.cos(rad)*(x-ctrx)-math.sin(rad)*(y-ctry)
    ry = math.sin(rad)*(x-ctrx)+math.cos(rad)*(y-ctry)
    newx = int(float(ctrx+rx-minx)/(maxx-minx)*scr_width)
    newy = scr_height - int(float(ctry+ry-miny)/(maxy-miny)*scr_height)
    return (newx, newy)

im = Image.new('RGB', (scr_width, scr_height), color="white")
draw = ImageDraw.Draw(im)
font = ImageFont.truetype("arial.ttf", 24)
smallfont = ImageFont.truetype("arial.ttf", 10)
title = "Population Distribution of NZ (2015)"
w,h = font.getsize(title)
x=(scr_width-w)/2
y =5 
draw.text((x, y), title, font=font, fill="black")
maxv = minv = None
geom = shpf.shapes()
for fidx, feature in enumerate(geom):
    try:
        if regidx[fidx] == 0: continue
        v = df.iloc[19, regidx[fidx]]
        print v
    except IndexError:
        continue
    if minv == None or v < minv: minv = v
    if maxv == None or v > maxv: maxv = v

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
        try:
            v = df.iloc[19, regidx[fidx]].astype(float) 
            greyness = maxgrey - (int((maxv-v)*(maxgrey-mingrey)/(maxv-minv)))
        except TypeError:
            import pdb; pdb.set_trace()
        #print greyness
        draw.polygon(poly_list, outline="blue", fill=(255-greyness,)*3)
        xm = (xs1+xs2)/2
        ym = (ys1+ys2)/2
        #draw.text((xm, ym), str(fidx+1), font=font, fill="black")


#print poly_list
print (minv, maxv)
legend_box = (440,300,470,390)
lmargin = 20
height = legend_box[3]-legend_box[1] 
maxgrey1 = maxgrey + lmargin 
mingrey1 = mingrey - lmargin 
for iy in range(legend_box[1], legend_box[3]):
    greyness = int(maxgrey1 - float(maxgrey1-mingrey1)/(height)*(iy - legend_box[1]))
    #print greyness
    draw.line((legend_box[0], iy) + (legend_box[2], iy), fill=(255-greyness,)*3)
    
draw.rectangle(legend_box, outline="blue")

nticks = 4
ticklen = 10
divisor = 6
vmargin = float(lmargin)/(maxgrey-mingrey)*height
s = "(million)"
w,h = smallfont.getsize(s)
draw.text(((legend_box[2]+legend_box[0]-w)/2, legend_box[1]-h-3),s,
    font=smallfont, fill="blue")

for ii in range(0, nticks):
    v = maxv - float(maxv-minv)*ii/(nticks-1)
    s = "%.2f" % (v/10**divisor)
    w,h = smallfont.getsize(s)
    print "*"+s+"*"
    vpos = float(ii)*(height-2*vmargin)/(nticks-1)+vmargin+legend_box[1]
    draw.text((legend_box[0]-ticklen-w-3, vpos-h/2), s, font=smallfont, fill="blue")
    print vpos
    draw.line((legend_box[0]-ticklen, vpos) + (legend_box[0], vpos), fill="blue")


del draw
im.save("nz1.png", "PNG")
