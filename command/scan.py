#!/usr/bin/env python3
import random,copy
from .read.readSLHA import readSLHA
from .sampleoperation.generate import *

class Parameter:
    def __init__(self,name,block,PDG,value):
        self.name   =   name
        self.block  =   block
        self.PDG    =   PDG
        self.value  =   value

class Variable(Parameter):
    def __init__(self,name,block,PDG,min,max,walk='flat',step=None,value=None):
        Parameter.__init__(self,name,block,PDG,value)
        self.max    =   float(max)
        self.min    =   float(min)
        self.walk   =   walk
        self.step   =   step

class ParameterSpace(Variable):
    def __init__(self):
        self.VariableList=[]
    def Add(self,name,block,PDG,min,max,walk='flat',step=None,value=None):
        setattr(self,name,Variable(name,block,PDG,min,max,walk,step,value))
        self.VariableList.append(name)
        if not hasattr(self,block):
            setattr(self,block,{})
        getattr(self,block)[PDG]=getattr(self,name)
        getattr(self,block)[name]=getattr(self,name)

class Sample():
    def __init__(self,scan='random'):
        self.free=ParameterSpace()
        self.quantities=readSLHA()
        self.scan=scan
    def GetNew(self):
        new=copy.deepcopy(self.free)
        for name in new.VariableList:
            N=getattr(new,name)
            if type(N.walk) is str: 
                N.value=getattr(generate,self.scan+N.walk)(N)
            else:
                N.value=N.walk.value
        return new
    def GetValueFrom(self,inp):
        S=readSLHA()
        S.read(inp)
        ParameterList=self.free.VariableList
        BLOCK=''
        for name in ParameterList:
            Pari=getattr(self.free,name)
            Pari.value=getattr(S,Pari.block)[Pari.PDG]
            #print(name,Pari.value)
        return