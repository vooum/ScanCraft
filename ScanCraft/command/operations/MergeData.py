#!/usr/bin/env python3

def(base,addition):
    for key,value in addition.__dict__:
        new_key=key
        while hasattr(base,new_key):
            new_key=new_key+'n'
        setattr(base,new_key,value)