#!/usr/bin/env python3
import numpy,os

#print(__file__)
class DirectDetection:
    def __init__(self,exp):
        self.exp=exp
        Dir=os.path.dirname(__file__)
        self.line=numpy.loadtxt(os.path.join(Dir,exp))
    def value(self,mass):
        if mass<self.line[0,0]:
            exit('Entered mass value too small. Out of the range provided by '+repr(self.exp))
        for i in range(1,self.line.shape[0]):
            if mass < self.line[i,0]: 
                return self.line[i-1,1]+(mass-self.line[i-1,0])*(self.line[i,1]-self.line[i-1,1])/(self.line[i,0]-self.line[i-1,0])
        else:
            exit('Entered mass value too large. Out of the range provided by '+repr(self.exp))