#!/usr/bin/env python3
from .Experiments.colliders import EXP
def chi2(mu, data): 
    return (mu-data[0])**2/(data[1]**2+data[2]**2)
mh =[125.7, 0.4, 1.5]
bsg=[3.43, 0.21, 0.3]
bmu=[2.9, 0.7, 0.38]
omg=[0.1187,0.0117,0.0123]
gm2=[28.7,8.0,2.0]

X2Keys_defult='HiggsMass, b__Xs_gamma, bs__mu_mu, OMG'.split(', ')
LimitKeys_defult=[]
'''class constraints(EXP):
    def __init__(self,X2Keys=X2Keys_defult,LimitKeys=LimitKeys_defult):
        self.X2Keys=X2Keys
        self.LimitKeys=LimitKeys
        self.X2List={}
    
    def getX2(self,sample,**items):
        if len(items)==0:
            for item in self.X2Keys:
                obs=item
        else:
            for item,value in items.items():
                obs=EXP(item)
'''

def X2(**items):
    for item,value in items.items():
        obs=EXP(item)
        if obs.UB()!=None:
            if obs.LB()!=None:# both bound
                return (obs.v()-value)**2/((obs.v()-obs.LB())**+(obs.v()-obs.UB())**2)
            else:# Upper bound
                if value<obs.UB():
                    return 0.
                else:
                    return ((value-obs.UB())/obs.UB())**2
        else:#Lower bound
            if value>obs.UB():
                return 0.
            else:
                return ((value-obs.LB())/obs.LB())**2
            
if __name__=='__main__':
    print(X2(HiggsMass=123.))