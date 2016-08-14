#!/usr/bin/env python3
from command import *
#print([ i for i in globals().keys() if '__' not in i])


# settings
ism='M_h2'
target=5
StepFactor=1. # sigma = n% of (maximum - minimum) of the free parameters
SlopFactor=.3 # difficulty of accepting a new point with higher chisq
readstart=True
add_chisq=True

#print(read.readline.readline)
print(mcmc.Scan)

free=mcmc.Scan()
free.add('tanB','MINPAR'   ,3  ,2.     ,60.,value=15)
print(free.tanB.max)
print(getattr(free,'tanB',None).walk)
print(free.list)
print(free.tanB.value)
