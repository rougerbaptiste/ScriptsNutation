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
from skimage.filters import threshold_otsu, threshold_mean
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import sys
import pickle
from Tkinter import *
import Image, ImageTk
from numpy import savetxt, stack
import os
from scipy.interpolate import interp1d

PATH = sys.argv[1]
ReadEvery = int(sys.argv[2])
Scale = int(sys.argv[3])
XStart = int(sys.argv[4])
XStop = int(sys.argv[5])
spacePic = int(sys.argv[6])

files = [f for f in listdir(PATH) if isfile(join(PATH,f)) and '.jpg' in f]
files.sort()

imSize = io.imread(join(PATH,files[0]),plugin='matplotlib')
WIDTH = imSize.shape[1]
HEIGHT = imSize.shape[0]

linestopick = []

indexes = list(range(0, len(files), ReadEvery)) + [len(files)-1]
# print(indexes)
for ind in indexes:

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




        #function to be called when mouse is clicked
        def printcoords(event):
            #outputting x and y coords to console
            linestopick.append(event.y)
            root.destroy()
        #mouseclick event
        canvas.bind("<Button 1>",printcoords)

        root.mainloop()
print(linestopick)

f = interp1d(indexes, linestopick)
indicesFull = np.arange(0, len(files))

allLines = [int(e)*Scale for e in f(indicesFull)] # reconstitution of the indices for all pictures and not clicked ones
print(allLines)
# for ligne in linestopick:
#
#     for value in range(0, ReadEvery):
#         allLines.append(ligne*Scale)
#
# print(allLines)

# crop of pictures + TL creation + saving TL to color and gray
finalWidth = XStop - XStart
newLine = np.zeros(shape=(len(files), finalWidth, 3), dtype=np.uint8)

saveNb = 0
for index, fichier in enumerate(files):

    print(str(index+1) + "/" + str(len(files)))
    imFull = io.imread(join(PATH,fichier),plugin='matplotlib')
    newLine[index,:,:] = imFull[allLines[index], XStart:XStop]

    # save the pic with the red line
    if index % ReadEvery == 0:
        if not os.path.exists(join(PATH,"saves")):
            os.makedirs(join(PATH,"saves"))
        imRedL = np.zeros(shape=(imFull.shape), dtype=np.uint8)
        imRedL[0:allLines[index], :, :] = imFull[0:allLines[index]]
        imRedL[allLines[index],:,:] = [255,0,0]
        imRedL[allLines[index]+1:, :, :] = imFull[allLines[index]+1:]
        fname = "im" + str(saveNb) + "-" + str(index) + ".png"
        io.imsave(join(PATH, "saves", fname), img_as_uint(imRedL))
        saveNb+=1


pickle.dump([newLine[:,:,:]], open(join(PATH, "pickle"), "w"))
filename = 'TLCol' + '.png'
io.imsave(join(PATH, filename), img_as_uint(newLine[:,:,:]))
tlGray = rgb2gray(newLine[:,:,:])
filename = 'TLGray' + '.png'
io.imsave(join(PATH, filename), img_as_uint(tlGray))


# computes the position of the leaf
g = io.imread(join(PATH, "TLGray.png"),plugin='matplotlib')
pos = []
ind = []
for i in np.arange(len(g[:,0])):
	signal = g[i,:] -np.median(g[i,:])
	indices = np.where(signal> 0.5*max(signal))
	resu = np.median(indices)
	pos.append(resu)
	ind.append(i)

# saves the position to csv
indi = [e*spacePic for e in ind]
savetxt(join(PATH, "trajec.csv"), stack((indi, pos)), delimiter=',' )
plt.plot(indi, pos, "+-")

plt.savefig(join(PATH,"trajec.pdf"))
