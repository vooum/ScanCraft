#!/usr/bin/env python3

def AcquireAttr(obj,attr,value):
    if not hasattr(obj,attr):
        setattr(obj,attr,value)
    return getattr(obj,attr)

class lazyprogerty: # P271 in Python Cookbook
    def __init__(self,func):
        self.func=func
    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            value=self.func(instance)
            setattr(instance,self.func.__name__,value)
            return value