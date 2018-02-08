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

PATH = sys.argv[1]
WIDTH = int(sys.argv[2])
LINESTOPICK = sys.argv[3]
SHIFTSTART = int(sys.argv[4])
SHIFTSTOP = int(sys.argv[5])

linestopick = [int(e) for e in LINESTOPICK.split(',')]

files = [f for f in listdir(PATH) if isfile(join(PATH,f)) and '.jpg' in f]
files.sort()

deltaT = (SHIFTSTOP-SHIFTSTART)/len(files)

newLine = np.zeros(shape=(len(files), WIDTH, 3, len(linestopick)), dtype=np.uint8)
for index, fichier in enumerate(files):

    print(str(index+1) + "/" + str(len(files)))
    imFull = io.imread(join(PATH,fichier),plugin='matplotlib')
    for imgNb in range(0, len(linestopick)):
        newLine[index,:,:, imgNb] = imFull[linestopick[imgNb]+1 + int(index*deltaT)]


for imgNb in range(0,len(linestopick)):
    pickle.dump([newLine[:,:,:, imgNb]], open(join(PATH, "pickle" + str(linestopick[imgNb])), "w"))
    filename = 'TLCol' + str(linestopick[imgNb]) + '.png'
    io.imsave(join(PATH, filename), img_as_uint(newLine[:,:,:, imgNb]))
    tlGray = rgb2gray(newLine[:,:,:, imgNb])
    filename = 'TLGray' + str(linestopick[imgNb]) + '.png'
    io.imsave(join(PATH, filename), img_as_uint(tlGray))
    thresh = threshold_otsu(tlGray)
    binary = tlGray > thresh
    filename = 'TL' + str(linestopick[imgNb]) + '.png'
    io.imsave(join(PATH, filename), img_as_uint(binary))
