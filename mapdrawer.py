from PIL import Image, ImageDraw, ImageFont
import math
import types

class MapDrawer(object):
    img_width, img_height = 640, 480
    mingrey=20
    maxgrey=170


    def conv_coord(self, x,y, rot=10):
        ctrx = (self.maxx+self.minx)/2
        ctry = (self.maxy+self.miny)/2
        rad = rot*math.pi/180
        rx = math.cos(rad)*(x-ctrx)-math.sin(rad)*(y-ctry)
        ry = math.sin(rad)*(x-ctrx)+math.cos(rad)*(y-ctry)
        newx = int(float(ctrx+rx-self.minx)/(self.maxx-self.minx)*self.img_width)
        newy = self.img_height - int(float(ctry+ry-self.miny)/(self.maxy-self.miny)*self.img_height)
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

        minv = maxv = None
        for v in shades:
            if minv == None or v < minv: minv = v
            if maxv == None or v > maxv: maxv = v
        
        minx = miny = maxx = maxy = None
        for poly in polygons:
            for part in poly:
                for pt in part:
                    x,y = pt
                    if not minx or x < minx: minx = x
                    if not miny or y < miny: miny = y
                    if not maxx or x > maxx: maxx = x
                    if not maxy or y > maxy: maxy = y
        self.minx = int(minx - 0.15*(maxx-minx))
        self.miny = int(miny - 0.15*(maxy-miny))
        self.maxx = int(maxx + 0.15*(maxx-minx))
        self.maxy = int(maxy + 0.15*(maxy-miny))
        print (self.minx, self.miny, self.maxx, self.maxy)

        for idx, poly in enumerate(polygons):
            #x1,y1,x2,y2 = feature.bbox
            #xs1,ys1 = self.conv_coord(x1,y1)
            #xs2,ys2 = self.conv_coord(x2,y2)

            # create empty list to store all the coordinates
            v = shades[idx]
            greyness = self.maxgrey - (int((maxv-v)*(self.maxgrey-self.mingrey)/(maxv-minv)))
            for part in poly:
                poly_tuples = []
                for p in part:
                    x,y = self.conv_coord(p[0], p[1])
                    poly_tuples.append((x,y))

                if len(poly_tuples)>=2:
                    draw.polygon(poly_tuples, outline="blue", fill=(255-greyness,)*3)
                del poly_tuples
            #xm = (xs1+xs2)/2
            #ym = (ys1+ys2)/2
            #draw.text((xm, ym), str(fidx+1), font=font, fill="black")


        print (minv, maxv)
        legend_box = (440,300,470,390)
        lmargin = 20
        height = legend_box[3]-legend_box[1] 
        maxgrey1 = self.maxgrey + lmargin 
        mingrey1 = self.mingrey - lmargin 
        for iy in range(legend_box[1], legend_box[3]):
            greyness = int(maxgrey1 - float(maxgrey1-mingrey1)/(height)*(iy - legend_box[1]))
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
            vpos = float(ii)*(height-2*vmargin)/(nticks-1)+vmargin+legend_box[1]
            draw.text((legend_box[0]-ticklen-w-3, vpos-h/2), s, font=smallfont, fill="blue")
            draw.line((legend_box[0]-ticklen, vpos) + (legend_box[0], vpos), fill="blue")


        del draw
        return im

