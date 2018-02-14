#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This script is used to create the timeline picture of the leaf

@author: baptiste
"""

from os import listdir
from os.path import isfile, join
import numpy as np
from skimage import io, img_as_uint, img_as_float
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import sys
import pickle
from Tkinter import *
import Image, ImageTk

PATH = sys.argv[1]
ReadEvery = int(sys.argv[2])
Scale = int(sys.argv[3])
# WIDTH = int(sys.argv[2])
# LINESTOPICK = sys.argv[2]
# SHIFTSTART = int(sys.argv[2])
# SHIFTSTOP = int(sys.argv[3])

###
# Files finding and line choice

# linestopick = [int(e) for e in LINESTOPICK.split(',')]

files = [f for f in listdir(PATH) if isfile(join(PATH,f)) and '.jpg' in f]
files.sort()

imSize = io.imread(join(PATH,files[0]),plugin='matplotlib')
WIDTH = imSize.shape[1]
HEIGHT = imSize.shape[0]

linestopick = []

for ind in range(0, len(files), ReadEvery):
    # imLine = io.imread(join(PATH, files[ind]), plugin='matplotlib')

    if __name__ == "__main__":
        root = Tk()

        image = Image.open(join(PATH, files[ind]))
        [imageSizeWidth, imageSizeHeight] = image.size
        newImageSizeWidth = int(imageSizeWidth/Scale)
        newImageSizeHeight = int(imageSizeHeight/Scale)

        image = image.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)


        width = WIDTH
        height = HEIGHT
        root.minsize(width=newImageSizeWidth, height=newImageSizeHeight)

        #setting up a tkinter canvas with scrollbars
        frame = Frame(root, bd=2, relief=SUNKEN)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        xscroll = Scrollbar(frame, orient=HORIZONTAL)
        xscroll.grid(row=1, column=0, sticky=E+W)
        yscroll = Scrollbar(frame)
        yscroll.grid(row=0, column=1, sticky=N+S)
        canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        canvas.grid(row=0, column=0, sticky=N+S+E+W)
        xscroll.config(command=canvas.xview)
        yscroll.config(command=canvas.yview)
        frame.pack(fill=BOTH,expand=1)

        canvas.create_image(0,0,image=img,anchor="nw")
        canvas.config(scrollregion=canvas.bbox(ALL))


        #adding the image
        #File = askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
        # img = ImageTk.PhotoImage(Image.open(join(PATH, files[ind])))



        #function to be called when mouse is clicked
        def printcoords(event):
            #outputting x and y coords to console
            linestopick.append(event.y)
            root.destroy()
        #mouseclick event
        canvas.bind("<Button 1>",printcoords)

        root.mainloop()
print(linestopick)

allLines = []
for ligne in linestopick:
    for value in range(0, ReadEvery):
        allLines.append(ligne*Scale)

print(allLines)


newLine = np.zeros(shape=(len(files), WIDTH, 3), dtype=np.uint8)
for index, fichier in enumerate(files):

    print(str(index+1) + "/" + str(len(files)))
    imFull = io.imread(join(PATH,fichier),plugin='matplotlib')
    print(newLine[index,:,:].shape)
    print(imFull[allLines[index]+1].shape)
    newLine[index,:,:] = imFull[allLines[index]+1]
    # for imgNb in range(0, len(linestopick)):
    #     newLine[index,:,:, imgNb] = imFull[linestopick[imgNb]+1 + int(index*deltaT)]


# for imgNb in range(0,len(linestopick)):
pickle.dump([newLine[:,:,:]], open(join(PATH, "pickle"), "w"))
filename = 'TLCol' + '.png'
io.imsave(join(PATH, filename), img_as_uint(newLine[:,:,:]))
tlGray = rgb2gray(newLine[:,:,:])
filename = 'TLGray' + '.png'
io.imsave(join(PATH, filename), img_as_uint(tlGray))
thresh = threshold_otsu(tlGray)
binary = tlGray > thresh
filename = 'TL' + '.png'
io.imsave(join(PATH, filename), img_as_uint(binary))
