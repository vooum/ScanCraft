#!/usr/bin/env python3
import random,math

class Parameter:
    def __init__(self,name,block,PDG,value):
        self.name   =   name
        self.block  =   block
        self.PDG    =   PDG
        self.value  =   value


class mcmcParameter(Parameter):

    def flat_walk(self,factor=1):
        run =   random.gauss(self.value,self.step*factor)
        #self.new_value  =   max( min(self.min,self.value) , min(max(self.max,self.value),run))
        self.new_value = max( self.min, min( self.max, run))

    def log_walk(self,factor=1):
        self.new_log    =   random.gauss(self.log,self.step*factor)
        run =   10.**self.new_log
        #self.new_value  =   max( min(self.min,self.value) , min(max(self.max,self.value), run))
        self.new_value = max( self.min, min( self.max, run))
        
    def follow(self,factor=1):
        self.new_value  =   self.walk.new_value
 
    def __init__(self,name,block,PDG,min,max,walk='flat',step=None,value=None):
        Parameter.__init__(self,name,block,PDG,value)
        self.max    =   float(max)
        self.min    =   float(min)
        self.walk   =   walk
        self.step   =   step
    def SetRandom(self):
        self.new_value=self.value
        if self.walk=='flat':
            if self.step==None:
                self.step = abs(self.max-self.min)/100.
            self.new=self.flat_walk
        elif self.walk=='log':
            self.log = math.log10(self.value)
            self.new_log=self.log
            self.logmax=math.log10(self.max)
            self.logmin=math.log10(self.min)
            if self.step==None:
                self.step = (math.log10( self.max)-math.log10(self.min))/100.
            self.new=self.log_walk
        elif type(self.walk)==type(self):
            self.new=self.follow


class Scan():
    def __init__(self):
        self.VariableList=[]
    
    def add(self,name,block,PDG,min,max,walk='flat',step=None,value=None):
        setattr(self,name,mcmcParameter(name,block,PDG,min,max,walk,step,value))
        self.VariableList.append(name)
        if not hasattr(self,block):
            setattr(self,block,{})
        getattr(self,block)[PDG]=getattr(self,name)
        getattr(self,block)[name]=getattr(self,name)
    def SetRandom(self):
        for i in self.VariableList:
            getattr(self,i).SetRandom()
    def GetNewPoint(self,factor=1):
        for i in self.VariableList:
            getattr(self,i).new(factor)
    def record(self):
        for i in self.VariableList:
            P=getattr(self,i)
            P.value=P.new_value
            if P.walk=='log':
                P.log=P.new_log
    def print(self):
        for i in self.VariableList:
            P=getattr(self,i)
            print(P.name,'\t',P.value)