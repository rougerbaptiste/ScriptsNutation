#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
THis script is used to recreate the trajectory from the timeline picture

@author: baptiste
"""

import matplotlib.pyplot as plt
from skimage import io
import itertools
from os import listdir
from os.path import isfile, join
#import waipy
from numpy import savetxt, stack
#from wavelets import WaveletAnalysis
#from scipy.optimize import leastsq
import sys

#fitfunc = lambda p, x :   ( p[0]  * np.exp(-((x-p[1])/p[2])**2) )
#errfunc = lambda p, x, y : fitfunc(p,x) - y




mypath = sys.argv[1]
myPic = sys.argv[2]
spacePic = int(sys.argv[3])

files = [f for f in listdir(mypath) if isfile(join(mypath,f)) and '.jpg' in f]

TL = io.imread(join(mypath, myPic))

trajec = []
for ligne in range(len(files)):
    positions = []
    pixSuite = []
    pixLine = TL[ligne, :]
    suite = 0
    for ind, pixel in enumerate(pixLine):
        if pixel!=0:
            suite += 1
            positions.append(ind)
            pixSuite.append(suite)
        else:
            suite = 0
    # find max de la suite
    maxSuite = [0]
    for pixS in range(0, len(pixSuite)):
        try:
            if pixSuite[pixS] >= pixSuite[pixS+1]:
                maxSuite.append(pixS)
                maxSuite.append(pixS+1)
        except:
            maxSuite.append(pixS)

    for pos in range(0, len(maxSuite), 2):
        max1 = maxSuite[pos]
        max2 = maxSuite[pos+1] +1
        pixSuite[max1:max2] = itertools.repeat(len(pixSuite[max1:max2]), len(pixSuite[max1:max2]))

    sumPix = 0
    for indMoy in range(0, len(pixSuite)):
        sumPix += positions[indMoy] * pixSuite[indMoy]
    sumPix /= sum(pixSuite)
    trajec.append(sumPix)

absc = [0]
for ind in range(0, len(trajec)-1):
    absc.append(absc[ind]+spacePic)

savetxt(join(mypath, "trajec.csv"), stack((absc, trajec)), delimiter=',' )
# fileWrite = open(join(mypath, "trajec.csv"), "a")
# #for i in range(0,len(absc)):
# #    lineToWrite = str(absc[i]) + ";" + str(trajec[i]) + "\n"
# #    fileWrite.write(lineToWrite)
# fileWrite.write(",".join(str(e) for e in absc) + "\n")
# #fileWrite.write("\n")
# fileWrite.write(",".join(str(e) for e in trajec))
# fileWrite.close()

plt.plot(absc, trajec, "+-")

plt.savefig(join(mypath,"trajec.pdf"))