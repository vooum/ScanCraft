#!/usr/bin/env python3
from command import NMSSMTools as NT
class Point():
    pass

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