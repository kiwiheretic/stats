from PIL import Image, ImageDraw, ImageFont
import shapefile
import math
import pandas as pd



class MapDrawer(object):
    img_width, img_height = 640, 480
    mingrey=20
    maxgrey=170

    def conv_coord(self, x,y, rot=10):
        minx, miny, maxx, maxy = 1000000, 4500000, 2600000, 6300000
        ctrx = (maxx+minx)/2
        ctry = (maxy+miny)/2
        rad = rot*math.pi/180
        rx = math.cos(rad)*(x-ctrx)-math.sin(rad)*(y-ctry)
        ry = math.sin(rad)*(x-ctrx)+math.cos(rad)*(y-ctry)
        newx = int(float(ctrx+rx-minx)/(maxx-minx)*self.img_width)
        newy = self.img_height - int(float(ctry+ry-miny)/(maxy-miny)*self.img_height)
        return (newx, newy)

    def draw(self, polygons, shades, bboxes=None, title=None, legend_header=None):
        im = Image.new('RGB', (self.img_width, self.img_height), color="white")
        draw = ImageDraw.Draw(im)
        smallfont = ImageFont.truetype("arial.ttf", 10)
        font = ImageFont.truetype("arial.ttf", 24)
        if title:
            w,h = font.getsize(title)
            x=(self.img_width-w)/2
            y =5 
            draw.text((x, y), title, font=font, fill="black")

        for idx, poly in enumerate(polygons):
            #x1,y1,x2,y2 = feature.bbox
            #xs1,ys1 = self.conv_coord(x1,y1)
            #xs2,ys2 = self.conv_coord(x2,y2)

            poly_tuples = []
            for p in poly:
                x,y = self.conv_coord(p[0], p[1])
                poly_tuples.append((x,y))

            #print (x1,y2,x2,y2)
            #print (xs1, ys1, xs2, ys2)
            # create empty list to store all the coordinates
            v = shades[idx]
            greyness = self.maxgrey - (int((maxv-v)*(self.maxgrey-self.mingrey)/(maxv-minv)))
            #print greyness
            if len(poly_tuples)>=2:
                draw.polygon(poly_tuples, outline="blue", fill=(255-greyness,)*3)
            del poly_tuples
                #draw.line(poly_list, fill="blue")
            #xm = (xs1+xs2)/2
            #ym = (ys1+ys2)/2
            #draw.text((xm, ym), str(fidx+1), font=font, fill="black")


        #print poly_list
        print (minv, maxv)
        legend_box = (440,300,470,390)
        lmargin = 20
        height = legend_box[3]-legend_box[1] 
        maxgrey1 = self.maxgrey + lmargin 
        mingrey1 = self.mingrey - lmargin 
        for iy in range(legend_box[1], legend_box[3]):
            greyness = int(maxgrey1 - float(maxgrey1-mingrey1)/(height)*(iy - legend_box[1]))
            #print greyness
            draw.line((legend_box[0], iy) + (legend_box[2], iy), fill=(255-greyness,)*3)
            
        draw.rectangle(legend_box, outline="blue")

        nticks = 4
        ticklen = 10
        divisor = 6
        vmargin = float(lmargin)/(self.maxgrey-self.mingrey)*height
        if legend_header:
            w,h = smallfont.getsize(legend_header)
            draw.text(((legend_box[2]+legend_box[0]-w)/2, legend_box[1]-h-3),legend_header,
                font=smallfont, fill="blue")

        for ii in range(0, nticks):
            v = maxv - float(maxv-minv)*ii/(nticks-1)
            s = "%.2f" % (v/10**divisor)
            w,h = smallfont.getsize(s)
            print "*"+s+"*"
            vpos = float(ii)*(height-2*vmargin)/(nticks-1)+vmargin+legend_box[1]
            draw.text((legend_box[0]-ticklen-w-3, vpos-h/2), s, font=smallfont, fill="blue")
            draw.line((legend_box[0]-ticklen, vpos) + (legend_box[0], vpos), fill="blue")


        del draw
        return im


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
maxv = minv = None
geom = shpf.shapes()
shades = []
polygons = []
bboxes = []
for fidx, feature in enumerate(geom):
    print len(feature.points)
    try:
        if regidx[fidx] == 0: continue
        v = df.iloc[19, regidx[fidx]]
        print v
        shades.append(v)
    except IndexError:
        continue
    polygons.append(feature.points)
    bboxes.append(feature.bbox)
    if minv == None or v < minv: minv = v
    if maxv == None or v > maxv: maxv = v

map1 = MapDrawer()
#img = map1.draw(polygons, shades, bboxes=bboxes, title="Population Distribution of NZ (2015)")
img = map1.draw(polygons, shades, bboxes=bboxes, legend_header="(million)")
img.save("nz1.png", "PNG")
