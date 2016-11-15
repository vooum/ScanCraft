#!/usr/bin/env python3
import sys,os,copy
from command import scan
from command.sampleoperation.getpoint import GetPoint

ignore=[ 'Landau Pole'
        ,'relic density'
        ,'Muon magn. mom.'
        ,'b -> c tau nu'
        ]

SampleModel=scan.ParameterSpace()
SampleModel.Add('tanB','MINPAR',3,2.,60.,step=None)
SampleModel.Add('M1','EXTPAR',1  ,20.    ,1000.,step=None)
SampleModel.Add('M2'	,'EXTPAR'   ,2  ,100.    ,2000.,step=None)
SampleModel.Add('Atop'	,'EXTPAR'   ,11  ,  -6e3    ,6e3,step=None)
SampleModel.Add('Abottom','EXTPAR'   ,12,-6e3,6e3,walk=SampleModel.Atop)
SampleModel.Add('Atau'	,'EXTPAR'   ,13  ,  100.      ,2000.,step=None)
SampleModel.Add('MtauL','EXTPAR'   ,33,	100.,	2.e3,walk=SampleModel.Atau)
SampleModel.Add('MtauR','EXTPAR'   ,36,	100.,	2.e3,walk=SampleModel.Atau)
SampleModel.Add('MQ3L'	,'EXTPAR'   ,43,	100.,	2.e3,step=None)
SampleModel.Add('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3,step=None)
SampleModel.Add('MbottomR','EXTPAR'  ,49,	100.,	2.e3 ,walk=SampleModel.MtopR)
SampleModel.Add('Lambda','EXTPAR'  ,61  ,1e-3    ,1. ,walk='log',step=None)
SampleModel.Add('Kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,walk='log',step=None)
SampleModel.Add('A_kappa','EXTPAR' ,64,-3.e3,3.e3,step=None)
SampleModel.Add('mu_eff','EXTPAR'  ,65,100.,1500.,step=None)
SampleModel.Add('MA','EXTPAR',124,	0.,	2.e3)
#get the folder to be rerun
print(copy.deepcopy(SampleModel).VariableList)
if len(sys.argv)>2:
    exit('too much argvs')
elif len(sys.argv)==1:
    exit('need path of the directory within samples to be run')
elif len(sys.argv)==2:
    SamplePool=sys.argv[1]
    if not os.path.isdir(SamplePool):
        exit(repr(SamplePool)+' is not a directory')

SampleList=[]
for file in os.listdir(SamplePool):
    name=os.path.join(SamplePool,file)
    SampleList.append(copy.deepcopy(SampleModel))
    GetPoint(SampleList[-1],name)
    SampleList[-1].infile=file

#print(len(SampleList))
for sample in SampleList:
    for comp in SampleList:
        if comp==sample:
            continue
        for par in SampleModel.VariableList:
            if getattr(sample,par).value!=getattr(comp,par).value:
                break
        else:
            print('equal')
            SampleList.remove(comp)
print(len(SampleList))
print([i.infile for i in SampleList])