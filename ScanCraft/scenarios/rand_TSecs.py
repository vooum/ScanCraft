#!/usr/bin/env python
# coding: utf-8

import sys,os,time,shutil,numpy
sys.path.append('/home/lifei/ScanCraft-New_ReadSLHA/ScanCraft')

from command.scan.scan import scan
from command.nexus.NMSSMTools import NMSSMTools

mold=scan(method="random")
mold.AddScalar('tanB','MINPAR',3,1.,60.)
mold.AddScalar('M1','EXTPAR',1  ,20.    ,1000.)
mold.AddScalar('M2','EXTPAR'   ,2  ,100.    ,2000.)
mold.AddScalar('Atop','EXTPAR'   ,11  ,  -6e3    ,6e3)
mold.AddFollower('Abottom','EXTPAR'   ,12,'Atop')
mold.AddScalar('Atau','EXTPAR'   ,13  ,  100.      ,2000.)
mold.AddFollower('MtauL','EXTPAR'   ,33,'Atau')
mold.AddFollower('MtauR','EXTPAR'   ,36,'Atau')
mold.AddScalar('MQ3L','EXTPAR'   ,43,	100.,	2.e3)
mold.AddScalar('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3)
mold.AddFollower('MbottomR','EXTPAR'  ,49,'MtopR')
mold.AddScalar('Lambda','EXTPAR'  ,61  ,1e-3    ,1. ,prior_distribution='exponential')
mold.AddScalar('Kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,prior_distribution='exponential')
mold.AddScalar('A_Lambda','EXTPAR' ,63,-3.e3,3.e3)
mold.AddScalar('A_kappa','EXTPAR' ,64,-3.e3,3.e3)
mold.AddScalar('mu_eff','EXTPAR'  ,65,100.,1500.)

os.chdir('/home/lifei/ScanCraft-New_ReadSLHA/ScanCraft/packages/NMSSMTools_5.5.3')
try:
    os.makedirs("output/record/random_20")
except FileExistsError:
    pass

N=NMSSMTools(input_mold="./SAMPLES/inpZ3.dat")
N.Make()

time_left = 2
i=0

good=[]

start = time.time()
while time.time()-start < 2:
    new_point=mold.Sample() 
    i+=1
    result=N.Run(new_point)
    if result.error:
        shutil.move("./inp", f"./output/record/random_20/inp.{i}.dat")
        good.append([i,0])
    else:
        N.Record(i)
        good.append([i,1])

good=numpy.array(good)
numpy.savetxt('./results',good)



