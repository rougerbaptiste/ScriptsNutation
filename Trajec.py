#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Ce script vise à retrouver numériquement la trajectoire de la plante

@author: baptiste
"""

#import os
#import matplotlib
import matplotlib.pyplot as plt
from skimage import io
#from skimage.filters import threshold_otsu
#from skimage.color import rgb2gray
#from skimage import novice
#import numpy as np
import itertools
from os import listdir
from os.path import isfile, join
import waipy
import numpy as np
from wavelets import WaveletAnalysis
#import wavelets
#import pywt
from scipy.optimize import leastsq

#def gauss (x, a, b, c):
#    return a * np.exp(-((x-b)/c)**2)

fitfunc = lambda p, x :   ( p[0]  * np.exp(-((x-p[1])/p[2])**2) )
errfunc = lambda p, x, y : fitfunc(p,x) - y


mypath = "./"
spacePic = 5

files = [f for f in listdir(mypath) if isfile(join(mypath,f)) and '.jpg' in f]

TL = io.imread("TL2.png")

trajec = []
for ligne in range(len(files)):
    positions = []
    pixSuite = []
#    print(ligne)
    pixLine = TL[ligne, :]
    suite = 0
    for ind, pixel in enumerate(pixLine):
        # print(pixel)
        if pixel!=0:
            suite += 1
            positions.append(ind)
            pixSuite.append(suite)
        else:
            suite = 0
    # print(pixSuite)
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
        # print(maxSuite[pos], maxSuite[pos+1])
        max1 = maxSuite[pos]
        max2 = maxSuite[pos+1] +1
        pixSuite[max1:max2] = itertools.repeat(len(pixSuite[max1:max2]), len(pixSuite[max1:max2]))
    # print(pixSuite)
        # pixSuite[maxSuite[pos]:maxSuite[pos+1]] = pixSuite[maxSuite[pos+1]]
    # print(positions, pixSuite, maxSuite)
    
    sumPix = 0
    for indMoy in range(0, len(pixSuite)):
        sumPix += positions[indMoy] * pixSuite[indMoy]
    sumPix /= sum(pixSuite)
    # print(sumPix)
    trajec.append(sumPix)

absc = [0]
for ind in range(0, len(trajec)-1):
    absc.append(absc[ind]+spacePic)

plt.plot(absc, trajec, "+")

plt.savefig("trajec.pdf")
#plt.show()
#print(trajec)

data_norm = waipy.normalize(trajec)
print(data_norm)

dt = spacePic

wavelet = 'morl'

plt.plot(absc, data_norm)
 

wa = WaveletAnalysis(data_norm, dt=spacePic)
power = wa.wavelet_power
scales = wa.scales
t = wa.time
rx = wa.reconstruction()
pp = wa.fourier_periods


fig, ax = plt.subplots()
T, S = np.meshgrid(t, scales)
ax.contourf(T, S, power, 100)
ax.set_yscale('log')
fig.savefig("zzzz.pdf")

plt.figure()
plt.plot(scales, power[:,1000])
plt.xlabel('Echelle')
plt.ylabel('Energie')

plt.figure()
plt.plot(pp, power[:,1000], "-+")
plt.xlabel('Periodes equivalentes')
plt.ylabel('Energie')

#plt.show()
plt.close()
plt.close()
plt.close()
plt.close()
plt.close()

indices1 = np.where(pp<300)[0] # and pp > 50)
#indices2 = np.where(pp > 50)
#indices = [i for i in indices1]
freq = []
ampl = []
p0values=[10,100,25]
for i in range(0, len(power[1,:])):
#    freq.append(pp[np.argmax(power[indices1,i])])
    ydata = power[indices1, i]
    xdata = pp[indices1]
    print(indices1)
    p_solus, success =  leastsq(errfunc,p0values[:],args=(xdata, ydata))

    yfit = fitfunc(p_solus,xdata)
    
    freq.append(p_solus[1])
    ampl.append(p_solus[0])


#    print(popt)
#    if i == 1000:
#        plt.plot(xdata,ydata,'sb',label='data')
#        xdata2 = np.linspace(xdata[0], xdata[-1], 200)
#        plt.plot(xdata2,fitfunc(p_solus, xdata2),'r',label='fit')


plt.plot(freq)
plt.figure()
plt.plot(ampl)
plt.show()




