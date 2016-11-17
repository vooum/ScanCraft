#!/usr/bin/env python3
from command.scan import Sample
import command.darkmatter as DarkMatter




sample=Sample(scan='random')
free=sample.free
free.Add('tanB','MINPAR',3,2.,60.,step=None)
free.Add('M1','EXTPAR',1  ,20.    ,1000.,step=None)
free.Add('M2'	,'EXTPAR'   ,2  ,100.    ,2000.,step=None)
free.Add('Atop'	,'EXTPAR'   ,11  ,  -6e3    ,6e3,step=None)
free.Add('Abottom','EXTPAR'   ,12,-6e3,6e3,walk=free.Atop)
free.Add('Atau'	,'EXTPAR'   ,13  ,  100.      ,2000.,step=None)
free.Add('MtauL','EXTPAR'   ,33,	100.,	2.e3,walk=free.Atau)
free.Add('MtauR','EXTPAR'   ,36,	100.,	2.e3,walk=free.Atau)
free.Add('MQ3L'	,'EXTPAR'   ,43,	100.,	2.e3,step=None)
free.Add('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3,step=None)
free.Add('MbottomR','EXTPAR'  ,49,	100.,	2.e3 ,walk=free.MtopR)
free.Add('Lambda','EXTPAR'  ,61  ,1e-3    ,1. ,walk='log',step=None)
free.Add('Kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,walk='log',step=None)
free.Add('A_kappa','EXTPAR' ,64,-3.e3,3.e3,step=None)
free.Add('mu_eff','EXTPAR'  ,65,100.,1500.,step=None)
free.Add('MA','EXTPAR',124,	0.,	2.e3)

sample.GetValueFrom('inp.dat')
new=sample.free
print(repr([new.tanB.value,new.Lambda.value]))
LUXPsi=DarkMatter.DirectDetection('LUX201608_Psi.txt')#LUX