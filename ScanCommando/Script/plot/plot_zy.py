#!/usr/bin/env python

import os
import re 
import random
import matplotlib.pyplot as plt
from numpy import *

mandir=os.getcwd()

###################################################

data2 = loadtxt(r"obs.txt")


oft1    = abs(data2[:,7])
oft2    = abs(data2[:,8])
oft3    = abs(data2[:,9])
oft4    = abs(data2[:,10])
mu      = data2[:,11]
mh      = data2[:,2]


sel1 = (mh < 127) & (mh>123)


oft = array([max(oft1[i],oft2[i],oft3[i],oft4[i]) for i in range(len(oft1))])

print len(oft)
plt.figure(figsize=(10,10), dpi=70)
plt.semilogy(mu, oft,'.',color="r",markersize=15)

plt.xlabel(r"$\mu$",fontsize=24)
plt.ylabel(r"$\Delta_{BG}$",fontsize=24)


plt.savefig("fig01.png",dpi=150)

plt.figure(figsize=(10,10), dpi=70)
plt.plot(mu, mh,'.',color="red",markersize=15)

plt.xlabel(r"$\mu$",fontsize=24)
plt.ylabel(r"$m_h$",fontsize=24)


plt.savefig("fig02.png",dpi=150)