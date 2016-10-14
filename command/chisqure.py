#!/usr/bin/env python3
def chi2(mu, data): 
    return (mu-data[0])**2/(data[1]**2+data[2]**2)
mh =[125.7, 0.4, 1.5]
bsg=[3.43, 0.21, 0.3]
bmu=[2.9, 0.7, 0.38]
omg=[0.1187,0.0117,0.0123]
gm2=[28.7,8.0,2.0]