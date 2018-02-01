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

[absc, trajec] = np.loadtxt(join(mypath, myfile), delimiter=',')

trajecScaled = [a * myscale for a in trajec]

plt.figure()
plt.plot(absc, trajecScaled, '+-')
plt.savefig(join(mypath, "trajScaled.pdf"))

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
ax.contourf(T, S, power, 100)
ax.set_yscale('log')
fig.savefig(join(mypath,"powergraph.pdf"))

indices1 = np.where(pp<300)[0]
indices2 = np.where(pp > 50)[0]

indices1 = indices1.tolist()
indices2 = indices2.tolist()


indices = set(indices1).__and__(set(indices2))
indices = list(indices)
#print(indices)
freq = []
ampl = []
p0values=[10,100,25]

for i in range(0, len(power[1,:])):
    ydata = power[indices, i]
    xdata = pp[indices]
    p_solus, success =  leastsq(errfunc,p0values[:],args=(xdata, ydata))

    yfit = fitfunc(p_solus,xdata)

    freq.append(p_solus[1])
    ampl.append(p_solus[0])

amplScaled = [e * myscale for e in ampl]

plt.figure()
plt.plot(absc, freq, '+')
plt.savefig(join(mypath,"period.pdf"))
plt.figure()
plt.plot(absc, amplScaled, '+')
plt.savefig(join(mypath,"Zamplitude.pdf"))
