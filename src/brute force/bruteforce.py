from PIL import Image
import math
import string
import numpy as np
import random

from Captcha import Captcha
from Letter import Letter

import os
from os import listdir
from os.path import isfile, join

def filter_image_black(pixels):
        for y in range(15):
            for x in range(15):
                r, g, b, a = pixels[x,y]
                if (r<100):
                    pixels[x,y]= 0, 0, 0, 255
                else:
                    pixels[x,y]= 255,255,255, 255
        return pixels

def compare_pixels(pixels1, pixels2):
    total = 0.0
    correct = 0.0
    
    for x in range(0, 15):
        for y in range(0, 15):
            
            r1,g1,b1 = pixels1[x,y]
            r2,g2,b2, a = pixels2[x,y]
            #print pixels1[x,y]
            #print pixels2[x,y]
            if (r1==0 or r2==0):
                if (r1==r2 and g1==g2 and b1==b2):
                    total+=1
                    correct+=1
                else:
                    total+=1.0
        
    return (float)(correct/total)

def bruteforce_char(pixels):
    digit_filepaths = [digit[0] for digit in os.walk('../../data/processed/chars/digits')]
    uppercase_filepaths = [uppercase[0] for uppercase in os.walk('../../data/processed/chars/uppercase')]
    lowercase_filepaths = [lowercase[0] for lowercase in os.walk('../../data/processed/chars/lowercase')]    
    
    digit_filepaths.pop(0)
    uppercase_filepaths.pop(0)
    lowercase_filepaths.pop(0)
    
    max_perc = 0
    max_char = None
    max_filepath = None
    
    print "----Comparing to digits"
    for filepath in digit_filepaths:
        print "-----Comparing to: " + filepath
        filenames = [ f for f in listdir(filepath) if isfile(join(filepath,f))]
        for filename in filenames:
            if "_" in filename:
                pass
            else:
                print "------Comparing to: " +filename
                char_im = Image.open(filepath+"/"+filename)
                char_pixels = char_im.load()
                char_pixels = filter_image_black(char_pixels)
               # print char_pixels
                perc = compare_pixels(pixels,char_pixels)
                print "------Result: "+filename+" = "+str(perc)
                if (perc>max_perc):
                    max_perc = perc
                    chars = filepath.split("/")
                    max_char = chars[-1]
                    max_filepath = filepath+"/"+filename
    
    print "----Comparing to uppercase"
    for filepath in uppercase_filepaths:
        print "-----Comparing to: " + filepath
        filenames = [ f for f in listdir(filepath) if isfile(join(filepath,f))]
        for filename in filenames:
            if "_" in filename:
                pass
            else:
                print "------Comparing to: " +filename
                char_im = Image.open(filepath+"/"+filename)
                char_pixels = char_im.load()
                
                char_pixels = filter_image_black(char_pixels)
                
                perc = compare_pixels(pixels,char_pixels)
                print "------Result: "+filename+" = "+str(perc)
                if (perc>max_perc):
                    max_perc = perc
                    chars = filepath.split("/")
                    max_char = chars[-1]
                    max_filepath = filepath+"/"+filename
    
    print "----Comparing to lowercase"
    for filepath in lowercase_filepaths:
        print "-----Comparing to: " + filepath
        filenames = [ f for f in listdir(filepath) if isfile(join(filepath,f))]
        for filename in filenames:
            if "_" in filename:
                pass
            else:
                print "------Comparing to: " +filename
                char_im = Image.open(filepath+"/"+filename)
                char_pixels = char_im.load()
                print char_pixels[13,13]
                char_pixels = filter_image_black(char_pixels)
                print char_pixels[13,13]
                perc = compare_pixels(pixels,char_pixels)
                print "------Result: "+filename+" = "+str(perc)
                if (perc>max_perc):
                    max_perc = perc
                    chars = filepath.split("/")
                    max_char = chars[-1]
                    max_filepath = filepath+"/"+filename
    
    return max_perc, max_char, max_filepath
    
def process_char(pixels,avg_char_width, width, height,left_border):
    max_perc = 0
    max_char = None
    max_filepath = None
    max_right_border = 0
    max_im = None
    
    
    for j in range(-4,5):
        print "---Processing width :" + str(j)
        right_border = left_border+avg_char_width+j
        if (right_border>width):
            pass
        else:
            data = np.zeros((height, right_border-left_border, 3),dtype=np.uint8)
            for x in range(left_border, right_border):
                for y in range(height):
                    data[y][x-left_border] = pixels[x,y]
            char_im = Image.fromarray(data, 'RGB')
            letter = Letter(char_im)
            nonblank_rows = letter.find_nonblank_rows()
            letter.recreate_letter(nonblank_rows)
            letter.scale_down()
            
            
            perc, char, filepath = bruteforce_char(letter.pixels)
            
            print "---Done processing width :" + str(j)
            print "---Results: Max % = " + str(perc) + " for " + char
            
            if (perc>max_perc):
                max_perc = perc
                max_char = char
                max_filepath = filepath
                max_right_border = right_border
                max_im = letter.im
        
    #max_im.show()
    return max_perc, max_char, max_filepath, max_right_border
            
        

        
        

def process_data(pixels, width, height):
    print "-Starting to process data"
    avg_char_width = width/6
    left_border = 0
    chars = []
    percs = []
    filepaths =[]
    
    for i in range(0,6):
        print "--Processing char :" + str(i)
        perc, char, filepath, right_border = process_char(pixels,avg_char_width,width,height,left_border)
        print "--Finished processing char :" + str(i)
        print "--Results: Max % = " + str(perc) + " for " + char
        
        chars.append(char)
        percs.append(perc)
        filepaths.append(filepath)
        
        left_border=right_border
    
    print chars
    print percs
    print filepaths
    print left_border
    

        
def prep_data(filename, randnum):
    print "Starting to prepare data"
    filepath = '../../test/original/'+filename
    print "Opening original file at:" + filepath
    im = Image.open(filepath)

    captcha = Captcha(im)
    captcha.filter_image_red()
    captcha.find_original_corners()
    captcha.rotate_image()
    captcha.reset_minmax()
    captcha.find_rotated_sides()
    captcha.recreate_rectangle()
    captcha.filter_image_black()
    
    captcha.save_image(randnum)
    print "Finished preparing data"
    captcha.im.show()
    return captcha.im


if __name__ == "__main__":
    filenames = [ f for f in listdir('../../test/original') if isfile(join('../../test/original',f))]
    
    for filename in filenames:
        if "_" in filename:
            pass
        else:
            print "Beginning recognition for: " + filename
            randnum = random.randint(1,1000000)
            print "r: " + str(randnum)
            im = prep_data(filename, randnum)
            
            pixels = im.load()
            width, height = im.size
            
            process_data(pixels, width, height)
            
            

        