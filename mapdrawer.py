from PIL import Image, ImageDraw, ImageFont
import math
import types
import shapefile
class ShapeFileIterator(object):
    def __init__(self, filename):
        self.shpfile = filename
        self.shpf = shapefile.Reader(self.shpfile)
        self.geom = self.shpf.shapes()
        self.reset()

    def __iter__(self):
        return self

    def reset(self):
        self.gidx = 0

    def next(self):
        if self.gidx >= len(self.geom):
            raise StopIteration

        feature = self.geom[self.gidx]
        parts = []
        pidx2 = 0
        for idx in range(len(feature.parts)-1):
            pidx1 = feature.parts[idx]
            pidx2 = feature.parts[idx+1]
            parts.append(feature.points[pidx1:pidx2-1])
        self.gidx += 1
        parts.append(feature.points[pidx2:])
        return parts

class MapDrawer(object):
    mingrey=20
    maxgrey=170

    def __init__(self, dimensions = None):
        if dimensions:
            self.img_width, self.img_height = dimensions
        else:
            self.img_width, self.img_height = (640, 480)

        self.im = Image.new('RGB', (self.img_width, self.img_height), color="white")
        self._draw = ImageDraw.Draw(self.im)
        self.smallfont = ImageFont.truetype("arial.ttf", 10)
        self.font = ImageFont.truetype("arial.ttf", 24)
        self.regions = []

    def number_regions(self):
        if not self.regions:
            print "No regions to number"
            return

        cnt = 1
        for x,y in self.regions:
            self._draw.text((x, y), str(cnt), font=self.smallfont, fill="black")
            cnt += 1

    def conv_coord(self, x,y, rot=10):
        ctrx = (self.maxx+self.minx)/2
        ctry = (self.maxy+self.miny)/2
        rad = rot*math.pi/180
        rx = math.cos(rad)*(x-ctrx)-math.sin(rad)*(y-ctry)
        ry = math.sin(rad)*(x-ctrx)+math.cos(rad)*(y-ctry)
        newx = int(float(ctrx+rx-self.minx)/(self.maxx-self.minx)*self.img_width)
        newy = self.img_height - int(float(ctry+ry-self.miny)/(self.maxy-self.miny)*self.img_height)
        return (newx, newy)


    def draw(self, polygons, shades=None, bboxes=None, title=None, draw_legend = True, legend_header=None, use_divisor = False, exclude_regions=None, colour_profile=None):

        if title:
            w,h = self.font.getsize(title)
            x=(self.img_width-w)/2
            y =5 
            self._draw.text((x, y), title, font=self.font, fill="black")

        minv = maxv = None
        for v in shades:
            if not v: continue
            if minv == None or v < minv: minv = v
            if maxv == None or v > maxv: maxv = v
        
        minx = miny = maxx = maxy = None
        for ii, poly in enumerate(polygons):
            for part in poly:
                if exclude_regions and ii+1 in exclude_regions: continue
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
        self.regions = []

        if isinstance(polygons, ShapeFileIterator):
            polygons.reset()

        for idx, poly in enumerate(polygons):

            if not poly: continue
            if exclude_regions and idx+1 in exclude_regions: continue
            # create empty list to store all the coordinates
            if shades:
                v = shades[idx]
                if v:
                    greyness = self.maxgrey - (int((maxv-v)*(self.maxgrey-self.mingrey)/(maxv-minv)))
                else:
                    greyness = 0
            else:
                greyness = minv = maxv = v = 0

            if v:
                if colour_profile:
                    begin, end = colour_profile
                    fillcolour = []
                    for ii in range(3):
                        b = begin[ii]
                        e = end[ii]
                        c = int(0.9*(e-b)*(maxv - v)/(maxv-minv)+b)
                        fillcolour.append(c)
                    fillcolour = tuple(fillcolour)
                else:
                    fillcolour=(255-greyness,)*3
            else:
                fillcolour = (255,255,255)
            cnt = sx = sy = 0
            print fillcolour

            for part in poly:
                poly_tuples = []
                for p in part:
                    x,y = self.conv_coord(p[0], p[1])
                    poly_tuples.append((x,y))
                    sx += x
                    sy += y
                    cnt += 1

                if len(poly_tuples)>=2:
                    self._draw.polygon(poly_tuples, outline="blue", fill=fillcolour)
                del poly_tuples
            try:
                self.regions.append( (int(sx/cnt), int(sy/cnt) ))
            except ZeroDivisionError:
                import pdb 
                pdb.set_trace()


        if draw_legend:
            print (minv, maxv)
            legend_box = (self.img_width-70,300,self.img_width-40,390)
            lmargin = 20
            height = legend_box[3]-legend_box[1] 
            maxgrey1 = self.maxgrey + lmargin 
            mingrey1 = self.mingrey - lmargin 
            for iy in range(legend_box[1], legend_box[3]):
                if colour_profile:
                    begin, end = colour_profile
                    fillcolour = []
                    for ii in range(3):
                        b = begin[ii]
                        e = end[ii]
                        c = int((e-b)*float(iy-legend_box[1])/(height)+b)
                        fillcolour.append(c)
                    fillcolour = tuple(fillcolour)
                else:
                    greyness = int(maxgrey1 - float(maxgrey1-mingrey1)/(height)*(iy - legend_box[1]))
                    fillcolour=(255-greyness,)*3
                self._draw.line((legend_box[0], iy) + (legend_box[2], iy), fill=fillcolour)
                
            self._draw.rectangle(legend_box, outline="blue")

            nticks = 4
            ticklen = 10
            if use_divisor:
                divisor = int(math.log(maxv)/math.log(10))
            vmargin = 0.05*height
            if legend_header:
                w,h = self.smallfont.getsize(legend_header)
                self._draw.text(((legend_box[2]+legend_box[0]-w)/2, legend_box[1]-h-3),legend_header,
                    font=self.smallfont, fill="blue")

            for ii in range(0, nticks):
                v = maxv - float(maxv-minv)*ii/(nticks-1)
                if use_divisor:
                    s = "%.2f" % (v/10**divisor)
                else:
                    s = "%d" % v
                w,h = self.smallfont.getsize(s)
                vpos = float(ii)*(height-2*vmargin)/(nticks-1)+vmargin+legend_box[1]
                self._draw.text((legend_box[0]-ticklen-w-3, vpos-h/2), s, font=self.smallfont, fill="blue")
                self._draw.line((legend_box[0]-ticklen, vpos) + (legend_box[0], vpos), fill="blue")


        return self.im

    def __del__(self):
        del self._draw
