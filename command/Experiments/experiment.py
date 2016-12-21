#!/usr/bin/env python3

class LHC():
    HiggsMass=(125.7,125.3,127.2)
    
    b__Xs_gamma=(3.43e-4,2.99e-4,3.87e-4)
    bsg=b__Xs_gamma

    b__Xd_gamma=(1.41e-5,0.27e-5,2.55e-5)

    bs__mu_mu=(2.9e-9,1.7e-9,4.5e-9)
    bmu=bs__mu_mu

    OMG=(0.1197,0.1197*0.9,0.1197*1.1)

    # upper limit
    Z__h_a=5.78e-3




class exp(LHC):
    def value(name):
        return getattr(exp,name)[0]
    def LowerBound(name):
        data=getattr(exp,name)
        if len(data)==3:
            return data[1]
        else:
            exit(name+' has no lower 2 sigma bound')
    def UpperBound(name):
        data=getattr(exp,name)
        if len(data)==3:
            return data[2]
        else:
            exit(name+' has no upper 2 sigma bound')
    def UB(name):
        return exp.UpperBound(name)
    def LB(name):
        return exp.LowerBound(name)


def chi2(sample,X2List):
    for observable in X2List:
        print(observable)
        print()
        
        

if __name__=='__main__':
    class s():
        pass
    sample=s()
    sample.mh=120.
    #chi2(sample,['mh'])
    print(exp.value('HiggsMass'),exp.UB('HiggsMass'),exp.LB('bsg'))