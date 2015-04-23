from PIL import Image
import math
import numpy as np

class Captcha:
    
    ##average_char_width = 40 ##px wide
    
    def __init__(self, im):
        
        width, height = im.size
        
        self.width = width
        self.height = height
        self.im = im
        self.pixels = im.load()
        
        #Defining min values
        self.minx = 1000
        self.minxy = 0
        self.miny= 1000
        self.minyx = 0
        #Defining max values
        self.maxx = -1
        self.maxxy =0 
        self.maxy = -1
        self.maxyx = 0
        
    def filter_image_red(self):
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixels[x,y]
                if (r<245 and g<245 and b<245):
                    self.pixels[x,y]= 255, 0, 0
                else:
                    self.pixels[x,y]=255,255,255
                    
    def filter_image_black(self):
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixels[x,y]
                if (r!=255 or g!=255 or b!=255):
                    self.pixels[x,y]= 0, 0, 0
                else:
                    self.pixels[x,y]=255,255,255
                
                
    def find_original_corners(self):
        #Setting corners
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixels[x,y]
                if (r==255 and g==0 and b==0):
                    if (x<self.minx):
                        self.minx=x
                        self.minxy=y
                    if (x>self.maxx):
                        self.maxx=x
                        self.maxxy=y
                    if (y<self.miny):
                        self.miny=y
                        self.minyx=x
                    if (y>self.maxy):
                        self.maxy=y
                        self.maxyx=x
        #self.pixels[self.minx, self.minxy] = 150,150,150
        #self.pixels[self.maxx, self.maxxy] = 0,0,256
        #self.pixels[self.minyx, self.miny] = 256,0,0
        #self.pixels[self.maxyx, self.maxy] = 0,256,0
    
    def rotate_image(self):
        #captcha.im.show()
        
        if (self.minyx>self.width/2):
            print "leftdown"
            ydelta=float(self.maxy-self.maxxy)
            xdelta=float(self.maxx-self.maxyx)
            theta = math.atan(ydelta/xdelta)
            theta = theta*180/math.pi
            rotated_im = self.im.rotate(-theta)
        else:
            print "rightdown"
            ydelta=float(self.maxy-self.minxy)
            xdelta=float(self.maxyx-self.minx)
            ##print ydelta
            ##print xdelta
            theta = math.atan(ydelta/xdelta)
            print theta
            theta = theta*180/math.pi
            rotated_im = self.im.rotate(theta)
        #rotated_im.show()
        rotated_width, rotated_height = rotated_im.size
        self.width = rotated_width
        self.height = rotated_height
        self.im = rotated_im
        self.pixels = rotated_im.load()
        
    def reset_minmax(self):
        #Defining min values
        self.minx = 1000
        self.minxy = 0
        self.miny= 1000
        self.minyx = 0
        #Defining max values
        self.maxx = -1
        self.maxxy =0 
        self.maxy = -1
        self.maxyx = 0
    
    def find_rotated_sides(self):
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixels[x,y]
                if (r==255 and g==0 and b==0):
                    if (x<self.minx):
                        self.minx=x
                    if (x>self.maxx):
                        self.maxx=x
                    if (y<self.miny):
                        self.miny=y
                    if (y>self.maxy):
                        self.maxy=y
        

    def find_rows_with_color(pixels, width, height, color):
        rows_found=[]
        for y in xrange(height):
            for x in xrange(width):
                if pixels[x, y] != color:
                    break
                else:
                    rows_found.append(y)
        return rows_found

    def recreate_rectangle(self):
        width = abs(self.maxx-self.minx)+1
        height = abs(self.maxy-self.miny)+1
        # Creates a list containing 5 lists initialized to 0
        data = np.zeros((height, width, 3),dtype=np.uint8)
        for x in range(self.minx,self.maxx+1):
            for y in range(self.miny, self.maxy+1):
                if self.pixels[x, y]: ##<<<<
                    r, g, b = self.pixels[x, y]
                    if (r==0 and g==0 and b==0):
                        data[y-self.miny][x-self.minx]=[255,255,255]
                    else:
                        data[y-self.miny][x-self.minx]=self.pixels[x,y]
                else:
                    data[y-self.miny][x-self.minx]=[255,255,255]
        new_im = Image.fromarray(data, 'RGB')
        self.im = new_im
        self.pixels = new_im.load()
        width, height = new_im.size
        self.width = width
        self.height = height
    
    def find_nonblank_rows():
        rows_found=[]
        for y in xrange(height):
            color_found = False
            for x in xrange(width):
                r, g, b = pixels[x, y]
                if (r==255 and g==0 and b==0):
                    color_found = True
                else:
                    pass
            if color_found:
                rows_found.append(y)
        return rows_found
    
    def save_image(self, iternum):
        print "about to save"
        filepath = '../../data/prepped/raw/preppeddata'+str(iternum)+'.png'
        self.im.save(filepath)
        print "saved!"
        
def prep_data(iternum):
    filepath = '../../data/original/data'+str(iternum)+'.jpg'
    print filepath
    im = Image.open(filepath)
    #im.show()
    captcha = Captcha(im)
    
    captcha.filter_image_red()
    
    captcha.find_original_corners()
    
    captcha.rotate_image()
    
    captcha.reset_minmax()
    captcha.find_rotated_sides()
    captcha.recreate_rectangle()
    captcha.filter_image_black()
    #print "done"
    #captcha.im.show()
    captcha.save_image(iternum)
        

if __name__ == "__main__":
    prep_data(23)
    prep_data(24)
    #for i in xrange(1, 25):
        #prep_data(i)
        
    #prep_data(2)
#    im = Image.open("data21.jpg")
#    captcha = Captcha(im)
#    captcha.filter_image_red()
#    captcha.find_original_corners()
#    captcha.rotate_image()
#    captcha.reset_minmax()
#    captcha.find_rotated_sides()
#    captcha.recreate_rectangle()
#    captcha.filter_image_black()
#    captcha.im.show()

    

