from __future__ import division
import matplotlib.pyplot as picplot
from PIL import Image
import numpy as np
import math
import time

#Th following 3 lines get load the images into program and assign them variables
data_image = Image.open("data.png")
us_map = Image.open("us_outline.png")
us_maprecon = Image.open("us_outlinefinal.png")

#The following lines get the k amount of neighbors the user wants to aprrox. and ensures that is in within the testing parameters
k_neigh = 0
while k_neigh <=0 or k_neigh >69:
    k_neigh = raw_input("Please enter how many neighbors you would like to approximate(greater than 0 and less than 70): ")
    k_neigh = int(k_neigh)

start_time = time.time()


rests = []
w,h = data_image.size
data_image = np.float32(data_image)
us_map = np.float32(us_map)
us_maprecon = np.float32(us_maprecon)

#This block of for loops creates a list with meta data about where the restaurants are located on the map and what color they are.
for i in range (0,h):
    for j in range (0,w):
        if data_image[i][j][0] == 255 and data_image[i][j][1] == 0:
            rests.append(['r',i,j])
        elif data_image[i][j][0] == 255 and data_image[i][j][1] == 255:
            rests.append(['y',i,j])
        elif data_image[i][j][2] == 255:
            rests.append(['b',i,j])
        elif data_image[i][j][0] == 0 and data_image[i][j][1] == 0 and data_image[i][j][2] == 0:
            rests.append(['bla',i,j])
rests = sorted(rests)

#this block actually performs the math on distances for the every green pixel in the us map, and stores the distances and color in a 2d list temp
#then changes the color of the prixel based on the mean k nearest neighbors
for i in range (0,h):
    for j in range (0,w):
        if us_map[i][j][0]==0 and us_map[i][j][1]==255 and us_map[i][j][2]==0:
            pixel_color = np.array([0,0,0])
            temp =[]
            mean = 0
            for x in range (0, len(rests)):
                temp.append([math.sqrt(math.pow(i-rests[x][1],2)+(math.pow(j-rests[x][2],2))),rests[x][0]])
            temp = sorted(temp)
            for y in range (0, k_neigh):
                if temp[y][1] == 'r':
                    pixel_color[0]+=255
                elif temp[y][1] == 'y':
                    pixel_color[0]+=255
                    pixel_color[1]+=255
                elif temp[y][1] == 'b':
                    pixel_color[2]+=255
                   
            pixel_color = pixel_color/k_neigh
            us_maprecon[i][j] = pixel_color

#Shows the new reconstructed image and prints the time the program took            
us_maprecon = np.uint8(us_maprecon)      
picplot.imshow(us_maprecon)
print("%s seconds to run! " % (time.time() - start_time))    

