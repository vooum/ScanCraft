#!/usr/bin/env python3

class LHC():
    # (value, Minimum, Maximum)
    HiggsMass=(125.7,125.3,127.2)
    mh=HiggsMass

    b__Xs_gamma=(3.43e-4,2.99e-4,3.87e-4)
    bsg=b__Xs_gamma

    b__Xd_gamma=(1.41e-5,0.27e-5,2.55e-5)

    bs__mu_mu=(2.9e-9,1.7e-9,4.5e-9)
    bmu=bs__mu_mu

    Z__h_a=(None,None,5.78e-3)
class OtherEXPs():
    OMG=(0.1197,0.1197*0.9,0.1197*1.1)

    # upper limit

class EXP(LHC,OtherEXPs):
    def __init__(self,name):
        if type(name) is str:
            self.data=getattr(self,name)



def chi2(sample,X2List):
    X2_total=0.
    for observable in X2List:
        print(observable)


        
        

if __name__=='__main__':
    class s():
        pass
    sample=s()
    sample.mh=120.
    #chi2(sample,['mh'])
    print(EXP.value('HiggsMass'),EXP.UB('HiggsMass'),EXP.LB('bsg'),EXP.LB('Z__h_a'))
    print(EXP('b__Xd_gamma').value(),'aaaa')
    #print(LHC.__dict__)