#!/usr/bin/env python3

def AcquireAttr(obj,attr,value):
    if not hasattr(obj,attr):
        setattr(obj,attr,value)
    return getattr(obj,attr)

