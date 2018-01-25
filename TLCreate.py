#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
The script sert à recréer l'image qui représente le mouvement de la plante pour la nutation

@author: baptiste
"""

#import os
#import matplotlib
#import matplotlib.pyplot as plt
from skimage import io
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
#from skimage import novice
import numpy
#import itertools


# image = io.imread("./img_005,002_180116-155227.png")
# print(type(image))
# print(image.shape)

# image = rgb2gray(image)

# thresh = threshold_otsu(image)
# binary = image > thresh

from os import listdir
from os.path import isfile, join

mypath = "./"
lineToPick = 1620

files = [f for f in listdir(mypath) if isfile(join(mypath,f)) and '.jpg' in f]
files.sort()

# imTest = io.imread(join(mypath, files[0]), plugin='matplotlib')
# width = imTest.width
# print(width)


newLine = numpy.zeros(shape=(len(files), 4496))
# print(numpy.shape(newLine))
for index, fichier in enumerate(files):
    print(index)
    imFull = io.imread(join(mypath,fichier),plugin='matplotlib')
    imFull = rgb2gray(imFull)
    thresh = threshold_otsu(imFull)
    binary = imFull > thresh

    newLine[index, :] = binary[lineToPick+1]

io.imsave('test.png', newLine)