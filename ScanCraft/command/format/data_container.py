#!/usr/bin/env python3

class capsule():
    '''an empty class to store data in it,
    thus data can be accessed by .__dict__
    '''
    pass

def merge(*capsules):
    new_cps=capsule()
    for cps in capsules:
        for key,value in cps.__dict__.items():
            setattr(new_cps,key,value)
    return new_cps


# class shuttle():
#     def merge(self,*capsules):
#         self.cabin=merge(self.cabin,*capsules)