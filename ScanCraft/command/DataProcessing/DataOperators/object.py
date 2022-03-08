#!/usr/bin/env python3

def AcquireAttr(obj,attr,value):
    if not hasattr(obj,attr):
        setattr(obj,attr,value)
    return getattr(obj,attr)

class lazyproperty: # P271 in Python Cookbook
    def __init__(self,func):
        self.func=func
    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            value=self.func(instance)
            setattr(instance,self.func.__name__,value)
            return value

class lazyclass: # P271 in Python Cookbook
    def __init__(self,func,args):
        self.func=func
        self.args=args
    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            value=self.func(instance,*self.args)
            setattr(instance,self.func.__name__,value)
            return value