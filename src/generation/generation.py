from PIL import Image
import math
import string
import numpy as np

class Letter:
    
    
    def __init__(self, im):
        
        width, height = im.size
        
        self.width = width
        self.height = height
        self.im = im
        self.pixels = im.load()
        #print self.pixels[0,0]
        
        #Defining min values
        self.minx = 1000
        self.miny= 1000
        #Defining max values
        self.maxx = -1
        self.maxy = -1
        
    def find_sides(self):
        for y in range(self.height):
            for x in range(self.width):
                r, g, b, a = self.pixels[x,y]
                if (r==0 and g==0 and b==0):
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

    def recreate_letter(self, nonblank_rows):
        h = len(nonblank_rows)
        # Creates a list containing 5 lists initialized to 0
        data = np.zeros((h, self.width, 4),dtype=np.uint8)
        for i in xrange(h):
            y = nonblank_rows[i]
            for x in xrange(self.width):
                data[i][x] = self.pixels[x,y]
        
        new_im = Image.fromarray(data, 'RGBA')
        #new_im.show()
        self.im = new_im
        self.pixels = new_im.load()
        width, height = new_im.size
        self.width = width
        self.height = height
        
    def scale_down(self):
        resolution = 16
        spread = 1
        data = np.zeros((resolution, resolution, 4), dtype=np.uint8)
        for x in range(resolution):
            for y in range(resolution):
                
                yd = math.ceil((float)(y*self.height/resolution))
                xd = math.ceil((float)(x*self.width/resolution))
                
#                count = 0
#                num = 0
#                for i in range(-spread,spread+1):
#                    for j in range(-spread,spread+1):
#                        if (xd+i>-1 and xd+i<self.width and yd+j>-1 and yd+j<self.height):
#                            r,g,b,a = self.pixels[xd+i,yd+j]
#                            if (r!=255 or g!=255 or b!=255):
#                                count += 1
#                            num+=1
#                
#                perc = (float) (count/num)
#                if (perc>.5):
#                    data[y][x] = (0, 0, 0, 0)
#                else:
#                    data[y][x] = (255,255,255,255)
#                
#                        
#                        
                data[y][x] = self.pixels[xd, yd]
        new_im = Image.fromarray(data, 'RGBA')
        #new_im.show()
        self.im = new_im
        self.pixels = new_im.load()
        width, height = new_im.size
        self.width = width
        self.height = height
        
                
    
    def find_nonblank_rows(self):
        rows_found=[]
        for y in xrange(self.height):
            color_found = False
            for x in xrange(self.width):
                r, g, b, a = self.pixels[x, y]
                if (r!=255 or g!=255 or b!=255):
                    color_found = True
                else:
                    pass
            if color_found:
                rows_found.append(y)
        return rows_found
    
    def save_image(self, char):
        print "about to save"
        if (char in string.uppercase):
            filepath = '../../data/processed/chars/uppercase/'+char+'.png'
        elif (char in string.lowercase):
            filepath = '../../data/processed/chars/lowercase/'+char+'.png'
        elif (char in string.digits):
            filepath = '../../data/processed/chars/digits/'+char+'.png'
        else:
            print "error"
        self.im.save(filepath)
        print "saved!"
        
def generate_data(char):
    filepath = '../../data/unprocessed/'+char+'.png'
    print filepath
    im = Image.open(filepath)
    #im.show()
    if (char in string.uppercase):
        prepped_filepath = '../../data/prepped/chars/uppercase/'+char+'.png'
    elif (char in string.lowercase):
        prepped_filepath = '../../data/prepped/chars/lowercase/'+char+'.png'
    elif (char in string.digits):
        prepped_filepath = '../../data/prepped/chars/digits/'+char+'.png'
    else:
        print "error"
    im.save(prepped_filepath)
    letter = Letter(im)
    
    letter.find_sides()
    #letter.im.show()
    6
    nonblank_rows = letter.find_nonblank_rows()
    #print "nonblank_rows =" +str(nonblank_rows)
    letter.recreate_letter(nonblank_rows)
    #letter.im.show()
    letter.scale_down()
    #letter.im.show()
    
    #print "done"
    #captcha.im.show()
    letter.save_image(char)
        

#if __name__ == "__main__":
    #generate_data("8")
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

    

