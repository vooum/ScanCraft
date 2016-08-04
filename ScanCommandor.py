#!/usr/bin/env python3
from command import *
print([ i for i in globals().keys() if '__' not in i])


# settings
ism='M_h2'
target=5
StepNorm=1. # sigma = n% of (maximum - minimum) of the free parameters
SlopNorm=.3 # difficulty of accepting a new point with higher chisq
readstart=True
add_chisq=True

print(read.readline.readline)
