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
        self.new_value  =   max( min(self.min,self.value) , min(max(self.max,self.value),run))

    def log_walk(self,factor):
        self.new_log    =   random.gauss(self.log,self.step*factor)
        run =   10.**self.new_log
        self.new_value  =   max( min(self.min,self.value) , min(max(self.max,self.value), run))

    def follow(self):
        self.new_value  =   self.walk.new_value
 
    def __init__(self,name,block,PDG,min,max,walk='flat',step=None,value=None):
        Parameter.__init__(self,name,block,PDG,value)
        self.max    =   max
        self.min    =   min
        self.walk   =   walk
        self.step   =   step

        if walk=='flat':
            if step==None:
                self.step = abs(max-min)/100.
            self.new=flat_walk
        elif walk=='log':
            self.log = math.log10(self.value)
            if step==None:
                self.step = (math.log10( self.max)-math.log10(self.min))/100.
            self.new=log_walk
        elif type(walk)==type(self):
            self.new=follow
        self.new_value  =   None


class Scan():
    def __init__(self):
        self.list=[]
    
    def add(self,name,block,PDG,min,max,walk='flat',step=None,value=None):
        setattr(self,name,mcmcParameter(name,block,PDG,min,max,walk,step,value))
        self.list.append(name)
        if not hasattr(self,block):
            setattr(self,block,{})
        getattr(self,block)[PDG]=getattr(self,name)
        getattr(self,block)[name]=getattr(self,name)
    
    def GetNewPoint(self):
        for i in self.list:
            P=getattr(self,i)
    def record(self):
        for i in self.list:
            P=getattr(self,i)
            P.value=P.new_value
            if P.walk=='log':
                P.log=P.new_log
