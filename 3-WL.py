#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This script is used to analyze the trajetory using wavelets

@author: baptiste
"""

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
import sys

#def gauss (x, a, b, c):
#    return a * np.exp(-((x-b)/c)**2)

fitfunc = lambda p, x :   ( p[0]  * np.exp(-((x-p[1])/p[2])**2) )
errfunc = lambda p, x, y : fitfunc(p,x) - y

mypath = sys.argv[1]
myfile = sys.argv[2]

data = []
fileRead = open(join(mypath, myfile), "r")
for line in fileRead:
    data.append(map(int, line.split(",")))

trajec = data[0][:]
#print(trajec)
absc = data[1][:]
#print(absc)

data_norm = (trajec - np.mean(trajec))/np.std(trajec) # waipy.normalize(trajec)
#print(data_norm)


spacePic = absc[2] - absc[1]

wavelet = 'morl'

#plt.plot(absc, data_norm)
 
print("hi")
wa = WaveletAnalysis(data_norm, dt=spacePic)
print("ho")
power = wa.wavelet_power
scales = wa.scales
t = wa.time
#rx = wa.reconstruction()
pp = wa.fourier_periods

print("ha")

#fig, ax = plt.subplots()
#T, S = np.meshgrid(t, scales)
#ax.contourf(T, S, power, 100)
#ax.set_yscale('log')
#fig.savefig("zzzz.pdf")

#plt.figure()
#plt.plot(scales, power[:,1000])
#plt.xlabel('Echelle')
#plt.ylabel('Energie')

#plt.figure()
#plt.plot(pp, power[:,1000], "-+")
#plt.xlabel('Periodes equivalentes')
#plt.ylabel('Energie')
#
##plt.show()
#plt.close()
#plt.close()
#plt.close()
#plt.close()
#plt.close()

indices1 = np.where(pp<300)[0] # and pp > 50)
#indices2 = np.where(pp > 50)
#indices = [i for i in indices1]
freq = []
ampl = []
p0values=[10,100,25]

print("hy")
for i in range(0, len(power[1,:])):
#    freq.append(pp[np.argmax(power[indices1,i])])
    ydata = power[indices1, i]
    xdata = pp[indices1]
#    print(indices1)
    
    p_solus, success =  leastsq(errfunc,p0values[:],args=(xdata, ydata))

    yfit = fitfunc(p_solus,xdata)
    
    freq.append(p_solus[1])
    ampl.append(p_solus[0])
print("he")

#    print(popt)
#    if i == 1000:
#        plt.plot(xdata,ydata,'sb',label='data')
#        xdata2 = np.linspace(xdata[0], xdata[-1], 200)
#        plt.plot(xdata2,fitfunc(p_solus, xdata2),'r',label='fit')


plt.plot(freq)
plt.savefig(join(mypath,"freq.pdf"))
plt.figure()
plt.plot(ampl)
plt.savefig(join(mypath,"ampl.pdf"))




