#!/usr/bin/env python3

import random,math

def x2(a,b):# chisqure
    return a**2+b**2

def LargerThan1(a,b):#judge
    if a+b<1:
        return False
    else:
        return True

def accept(new,old):
    if new<old:
        return True
    elif random.random() < math.exp(slop*(old-new)):
        return True
    else:
        return False
# free
#start
record=open('rrr','w')
x,y=1,1
target=0
chisq=1.5e10

step=1
slop=1e-2


while target<1000:
    xnew=random.gauss(x,step)
    ynew=random.gauss(y,step)
    if not LargerThan1(xnew,ynew):
        continue
    chisqnew=x2(xnew,ynew)

    if accept(chisqnew,chisq):
        target+=1
        x,y=xnew,ynew
        chisq=chisqnew
        record.write(str(x)+'\t'+str(y)+'\n')
        print(target,x,y)
    
    
