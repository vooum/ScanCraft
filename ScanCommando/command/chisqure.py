#!/usr/bin/env python3
from .Experiments.colliders import EXP
#from Experiments.colliders import EXP
def chi2(mu, data): 
    return (mu-data[0])**2/(data[1]**2+data[2]**2)
mh =[125.09, 0.24, 0.24]
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
    sum=0.
    for item,value in items.items():
        obs=EXP(item).data
        if obs[2]!=None:
            if obs[0]!=None:# both bound
                sum+=(obs[1]-value)**2/((obs[1]-obs[0])**2+(obs[1]-obs[2])**2)
                continue
            else:# Upper bound
                if value<obs[2]:
                    sum+=0.
                    continue
                else:
                    sum+=((value-obs[2])/obs[2])**2
                    continue
        else:#Lower bound
            if value>obs[2]:
                sum+=0.
                continue
            else:
                sum+=((value-obs[0])/obs[0])**2
                continue
    return sum
            
if __name__=='__main__':
    print(X2(HiggsMass=123.,bsg=3.e-4))