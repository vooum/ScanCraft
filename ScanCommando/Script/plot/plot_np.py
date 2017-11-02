#!/usr/bin/env python3
### input './print list' to show the numbers and names of all parameters

import os,re,sys,copy
import matplotlib.pyplot as plt
import numpy as np

# functions===============================================
def input(data):
    d=[]
    for line in open(data,'r').readlines():
        c=[]
        for i in (line.rstrip('\n').rstrip('\t')).split('\t'):
            c.extend(i.split(':'))
        d.append(c)
    return np.asarray(d)

class GetData:
    def __init__(self,data):
        a=input(data)
        self.name=a[0,1::2].tolist()
        self.par=a[:,2::2].astype(float)
        self.number=a[:,0].astype(int)
    def Add(self,data):
        a=input(data)
        if len(self.number)==len(a[:,0].astype(int)):
            self.name.extend(a[0,1::2].tolist())
            self.par=np.hstack((self.par,a[:,2::2].astype(float)))
        else:
            print('check the line number')
            exit()
#=========================================================

#------------------ read data file  --------------------
par=GetData('AllParameters.txt')
par.Add('Ft.txt')
parlist=[par]   # add all parameter arrays here
if len(sys.argv)>1:
    if sys.argv[1]=='list':
        for p in parlist:
            print('*'*20)
            for i in range(len(p.name)):
                print(i,p.name[i])
        exit()

#print(par.name)
#print(par.par)
#print(par.number)
# Reduce ============================================
