#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This script is used to analyze the trajetory using wavelets

@author: baptiste
"""

import matplotlib.pyplot as plt
from os.path import join
import waipy
import numpy as np
from wavelets import WaveletAnalysis
#import wavelets

from scipy.optimize import leastsq
import sys

fitfunc = lambda p, x :   ( p[0]  * np.exp(-((x-p[1])/p[2])**2) )
errfunc = lambda p, x, y : fitfunc(p,x) - y

mypath = sys.argv[1]
myfile = sys.argv[2]
myscale = float(sys.argv[3])

fudgeFactor = 117.96610952

[absc, trajec] = np.loadtxt(join(mypath, myfile), delimiter=',')

trajecScaled = np.array([a * myscale for a in trajec])

fit = np.polyfit(absc, trajecScaled, 1)
derive = np.poly1d(fit)

corrections = np.array([derive(e) for e in absc])

absc = absc/60.0

plt.figure()
plt.plot(absc, trajecScaled, '+-')
plt.plot(absc, corrections)
plt.xlabel("Time (in h)")
plt.ylabel("Position of the stem (in cm)")
plt.savefig(join(mypath, "trajScaledRaw.pdf"))

trajScaledRaw = trajecScaled
trajecScaled = trajecScaled - corrections

plt.figure()
plt.plot(absc, trajecScaled, '+-')
plt.xlabel("Time (in h)")
plt.ylabel("Position of the stem (in cm)")
plt.savefig(join(mypath, "trajScaledCorr.pdf"))

data_mean = np.mean(trajecScaled)
data_sd = np.std(trajecScaled)
data_norm = waipy.normalize(trajecScaled)


spacePic = absc[2] - absc[1]

wavelet = 'morl'

wa = WaveletAnalysis(data_norm, dt=spacePic)
power = wa.wavelet_power
scales = wa.scales
t = wa.time
rx = wa.reconstruction()
pp = wa.fourier_periods


plt.figure()
fig, ax = plt.subplots()
T, S = np.meshgrid(t, scales)
img = ax.contourf(T, S, power, 100)
ax.set_yscale('log')
fig.colorbar(img)
fig.savefig(join(mypath,"powergraph.pdf"))

indices1 = np.where(pp<300/60.0)[0]
indices2 = np.where(pp > 50/60.0)[0]

indices1 = indices1.tolist()
indices2 = indices2.tolist()


indices = set(indices1).__and__(set(indices2))
indices = list(indices)
#print(indices)
freq = []
ampl = []
p0values=[10,100.0/60,25/60.0] #initial guess fit gaussienne

for i in range(0, len(power[1,:])):
    ydata = power[indices, i]
    xdata = pp[indices]
    p_solus, success =  leastsq(errfunc,p0values[:],args=(xdata, ydata))

    yfit = fitfunc(p_solus,xdata)

    # plt.figure()
    # plt.plot(xdata, ydata)
    # plt.plot(xdata, yfit, 'r')
    # plt.show()

    freq.append(p_solus[1])
    ampl.append(p_solus[0])

amplScaled = np.array(ampl) #[e * myscale for e in ampl]

amplCM = (amplScaled * data_sd) / fudgeFactor

plt.figure()
plt.plot(absc, freq, '+')
x1,x2,y1,y2 = plt.axis()
# plt.axis([x1, x2, 0, 3])
plt.savefig(join(mypath,"period.pdf"))
plt.figure()
plt.plot(absc, amplCM, '+')
x1,x2,y1,y2 = plt.axis()
# plt.axis([x1, x2, -1, 100])
plt.savefig(join(mypath,"Zamplitude.pdf"))

plt.figure()
plt.plot(freq, amplCM, "+")
plt.xlabel("Period")
plt.ylabel("Amplitude")
plt.savefig(join(mypath, "Zcorr.pdf"))
