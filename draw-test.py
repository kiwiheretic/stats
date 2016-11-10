from PIL import Image, ImageDraw, ImageFont
import shapefile

shp_folder = "C:/Users/Glenn/Documents/Stats/ShapeFiles/"
shpf = shapefile.Reader(shp_folder + "REGC2016_GV_Full.shp")
fields = shpf.fields
for name in fields:
    print name

records = shpf.records()

def conv_coord(x,y):
    minx, miny, maxx, maxy = 1000000, 4600000, 2600000, 6300000
    scr_width, scr_height = 640, 480
    newx = int(float(x-minx)/(maxx-minx)*scr_width)
    newy = scr_height - int(float(y-miny)/(maxy-miny)*scr_height)
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
        draw.polygon(poly_list, outline="blue", fill="lightblue")
        xm = (xs1+xs2)/2
        ym = (ys1+ys2)/2
        draw.text((xm, ym), str(fidx+1), font=font, fill="black")

        #for idx, line in enumerate(poly_list[1:]):
        #    last_line = poly_list[idx-1]
        #    draw.line(last_line+line, fill="blue")

#print poly_list


del draw
im.save("nz.png", "PNG")
