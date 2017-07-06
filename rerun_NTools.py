#!/usr/bin/env python3
import sys,os,re,copy,shutil
sys.path.append('/home/vooum/Desktop/ScanCommando')

from command.read.readSLHA import *
from command.NMSSMTools import *
from command.Experiments.directdetection import *
from command.outputfile import *
from command.scan import scan

print(sys.argv)

ignore=[ 'Landau Pole'
        ,'relic density'
        ,'Muon magn. mom.'
        ,'b -> c tau nu'
        ,'direct detection'
        ]

free=scan()
#free.add(name,block,PDG,min,max,walk='flat',step=None,value=None)
free.Add('tanB','MINPAR',3,2.,60.)
free.Add('M1','EXTPAR',1  ,20.    ,1000.)
free.Add('M2'	,'EXTPAR'   ,2  ,100.    ,2000.)
free.Add('Atop'	,'EXTPAR'   ,11  ,  -6e3    ,6e3)
free.Add('Abottom','EXTPAR'   ,12,-6e3,6e3,pace='follow Atop')
free.Add('Atau'	,'EXTPAR'   ,13  ,  100.      ,2000.)
free.Add('MtauL','EXTPAR'   ,33,	100.,	2.e3,pace='follow Atau')
free.Add('MtauR','EXTPAR'   ,36,	100.,	2.e3,pace='follow Atau')
free.Add('MQ3L'	,'EXTPAR'   ,43,	100.,	2.e3)
free.Add('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3)
free.Add('MbottomR','EXTPAR'  ,49,	100.,	2.e3 ,pace='follow MtopR')
free.Add('Lambda','EXTPAR'  ,61  ,1e-3    ,1. ,pace='lognormal')
free.Add('Kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,pace='lognormal')
free.Add('A_kappa','EXTPAR' ,64,-3.e3,3.e3)
free.Add('mu_eff','EXTPAR'  ,65,100.,1500.)
free.Add('MA','EXTPAR',124,	0.,	2.e3)

if len(sys.argv)==1:
    key='mcmc'
else:
    if sys.argv[1][-1]=='/':
        key=sys.argv[1][:-1]
    else:
        key=sys.argv[1]
if len(sys.argv)==3:
    OutSteam=sys.argv[2]
elif len(sys.argv)>3:
    exit('too much argv(argument value)s')
else:
    OutSteam='ReCalculated'
#if os.path.exists(OutSteam):exit('Directory '+ OutSteam +' already exist')
AnalysedDir=os.path.join(OutSteam,'record')
try:
    os.mkdir(OutSteam)
    os.mkdir(AnalysedDir)
except:
    pass
Data=DataFile(Dir=OutSteam)

spectrs={}
record='record'
for dirs in os.listdir():
    spectri=[]
    if key in dirs and os.path.isdir(dirs):
        for files in os.listdir(os.path.join(dirs,record)):
            #if files=='spectr.0':continue
            name=os.path.join(os.getcwd(),dirs,record,files)
            if 'spectr' in files and os.path.isfile(name) and 'from' not in files:
                spectri.append(name)
        spectri.sort(key=lambda x: int(re.findall(r'\d+',x)[-1]))
        spectrs[dirs]=spectri

L_Nsd=DirectDetection('PandaX_Nsd_2016.txt')
L_Psd=DirectDetection('PandaX_Psd_2016.txt')
L_Psi=DirectDetection('LUX201608_Psi.txt')

N=NMSSMTools(data_dir=OutSteam)
N.output_file='spectr_MG'
outNumber=0
for dirs in spectrs.keys():
    for files in spectrs[dirs]:
        free.GetValue(files)
        spectr=N.Run(free,ignore=ignore)
        if spectr.ERROR:print(spectr.SPINFO);continue
        if len(spectr.constraints)>0:print(spectr.SPINFO);continue

        inNumber=re.findall(r'\d+',files)[-1]
        outNumber+=1   # reNumber
        #outNumber=int(inNumber) #keep original Number

        Data.In('AllParameters.txt').record(spectr.MINPAR,spectr.EXTPAR,spectr.NMSSMRUN,Number=str(outNumber))
        #Data.In('DarkMatter.txt').record({'DMRD':spectr.ABUNDANCE[4]},spectr.NDMCROSSSECT,Number=outNumber)
        Data.In('Mass.txt').record(spectr.MASS,Number=outNumber)

        N.Record(outNumber)
        print('%i recorded'%outNumber)