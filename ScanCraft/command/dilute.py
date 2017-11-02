#!/usr/bin/env python3
import sys,os,copy,shutil,re
from command import scan
from command.sampleoperation.getpoint import GetPoint
from command.NMSSMTools import NMSSMTools

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
    if 'spectr.' in file:
        name=os.path.join(SamplePool,file)
        SampleList.append(copy.deepcopy(SampleModel))
        GetPoint(SampleList[-1],name)
        SampleList[-1].infile=name
        lenth=len(SampleList)
        if lenth%1000==0:
            print(lenth,' smaples recorded ...')
print(lenth,' samples recorded.\nanalysing...')
#print([i.infile for i in SampleList])
def near(sample1,sample2,factor=10000):
    if sample1.VariableList!=sample2.VariableList:
        exit('degree of freedom of two samples different')
    for par in sample1.VariableList:
        s1=getattr(sample1,par)
        s2=getattr(sample2,par)
        if abs(s1.value-s2.value)>(s1.max-s1.min)/factor:
            return False
    else:
        return True
#print(len(SampleList))
for sample in SampleList:
    for comp in SampleList:
        if comp==sample:
            continue
        else:
            if near(sample,comp):
                SampleList.remove(comp)

print(len(SampleList),' samples left.\nrecording samples into ./mcmc/record/')

for sample in SampleList:
    files=sample.infile
    number=re.findall(r'\d+',files)[-1]
    outspectr=os.path.join('mcmc/record/','spectr.'+number)
    shutil.copy(files,outspectr)
    shutil.copy(files.replace('spectr','inp'),outspectr.replace('spectr','inp'))
    shutil.copy(files.replace('spectr','omega'),outspectr.replace('spectr','omega'))
print('recording complate.')