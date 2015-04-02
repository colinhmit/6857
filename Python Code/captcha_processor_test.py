from PIL import Image
import math

im = Image.open("currenttest.jpg")
pixels=im.load()

width, height =im.size

minx = 1000
minxy = 0
miny= 1000
minyx = 0

maxx = -1
maxxy =0 
maxy = -1
maxyx=0

for y in range(height):
    for x in range(width):
        r, g, b = pixels[x,y]
        if (r<250 and g<250 and b<250):
            if (x<minx):
                minx=x
                minxy=y
            if (x>maxx):
                maxx=x
                maxxy=y
            if (y<miny):
                miny=y
                minyx=x
            if (y>maxy):
                maxy=y
                maxyx=x

if (maxyx>width/2):
    ydelta=maxxy-miny
    xdelta=maxx-minyx
    theta = math.atan(ydelta/xdelta)
    theta = theta*180/math.pi
    rotated_im = im.rotate(theta)
else:
    ydelta=minxy-miny
    xdelta=minx-minyx
    theta = math.atan(ydelta/xdelta)
    theta = theta*180/math.pi
    rotated_im =im.rotate(theta)

rotated_pixels = rotated_im.load()
rotated_width, rotated_height = rotated_im.size

minx = 1000
miny= 1000
maxx = -1
maxy = -1

for y in range(rotated_height):
    for x in range(rotated_width):
        r, g, b = rotated_pixels[x,y]
        if (r<250 and g<250 and b<250 and r>0 and g>0 and b>0):
            if (x<minx):
                minx=x
            if (x>maxx):
                maxx=x
            if (y<miny):
                miny=y
            if (y>maxy):
                maxy=y

for y in range(rotated_height):
    for x in range(rotated_width):
        if (x==minx or x==maxx):
            rotated_pixels[x,y] = (174,32,31)
        if (y==miny or y==maxy):
            rotated_pixels[x,y] = (174,32,31)



    
            
rotated_im.show()
##cropped_im = rotated_im.crop((minx,maxy,maxx,miny))
##cropped_im.load()
##cropped_im.show()

##pixels[minx, minxy] = (174,32,31)
##pixels[maxx, maxxy] = (174,32,31)
##pixels[minyx, miny] = (174,32,31)
##pixels[maxyx, maxy] = (174,32,31)
##im.show()
##        




