#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This script is used to create the timeline picture of the leaf

@author: baptiste
"""

from os import listdir
from os.path import isfile, join
import numpy as np
from skimage import io
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
import sys

PATH = sys.argv[1]
LINETOPICK = int(sys.argv[2])

files = [f for f in listdir(PATH) if isfile(join(PATH,f)) and '.jpg' in f]
files.sort()

newLine = np.zeros(shape=(len(files), 4496))
for index, fichier in enumerate(files):
    print(str(index+1) + "/" + str(len(files)))
    imFull = io.imread(join(PATH,fichier),plugin='matplotlib')
    imFull = rgb2gray(imFull)
    thresh = threshold_otsu(imFull)
    binary = imFull > thresh

    newLine[index, :] = binary[LINETOPICK+1]

io.imsave(join(PATH,'test.png'), newLine)