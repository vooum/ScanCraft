#!/usr/bin/env python3
from command import NMSSMTools as NT
class Point():
    pass

class f1():
    def p(self):
        print('aa')

class f2(f1):
    def __init__(self):
        print(hasattr(self,'p'))

print(hasattr(f2,'p'))

def pp():
    print('bb')

f1.p2=pp

f2.p2()
f2.p(f2)




exit()
p=Point()
p.name='M1'
p.value=0
p.block='EXTPAR'
p.PDG=1

PP=Point()
PP.list=['M1']
PP.M1=p
NT.GetStartPoint(PP,'inp.dat')

print(PP.M1.value)

