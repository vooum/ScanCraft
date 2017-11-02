#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

r=np.loadtxt('rrr')
plt.scatter(r[:,0],r[:,1],c=r[:,0]**2+r[:,1]**2,edgecolors=None)
cb=plt.colorbar()
cb.set_label('$\phi ^2$',fontsize=50)
plt.savefig('hhh1')