#!/usr/bin/env python3
import sys,os,re,copy,shutil
sys.path.append('/home/vooum/Desktop/ScanCommando')
sys.path.append('/home/heyangle/Desktop/ScanCommando/ScanCommando')

from command.read.readSLHA import *
from command.NMSSMTools import ReadNMSSMToolsSpectr
from command.Experiments.directdetection import *
from command.outputfile import *

print(sys.argv)

ignore=[ 'Landau Pole'
        ,'relic density'
        ,'Muon magn. mom.'
        ,'b -> c tau nu'
        ]

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
    OutSteam='Analysed'
if os.path.exists(OutSteam):exit('Directory '+ OutSteam +' already exist')
os.mkdir(OutSteam)
AnalysedDir=os.path.join(OutSteam,'record')
os.mkdir(AnalysedDir)
Data=DataFile(Dir=OutSteam)

# output files ===================================

# N2=open(os.path.join(OutSteam,'N2Decay'),'w')
# N3=open(os.path.join(OutSteam,'N3Decay'),'w')
# C1=open(os.path.join(OutSteam,'C1Decay'),'w')
#-------------- get all spectr and omega files
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

outNumber=0
for dirs in spectrs.keys():
    for files in spectrs[dirs]:
        spectr=ReadNMSSMToolsSpectr(files,ignore=ignore)
        if len(spectr.constraints)==0:
            inNumber=re.findall(r'\d+',files)[-1]
            outNumber+=1   # reNumber
            #outNumber=int(inNumber) #keep original Number

            Data.In('AllParameters.txt').record(spectr.MINPAR,spectr.EXTPAR,spectr.NMSSMRUN,Number=str(outNumber))
            Data.In('DarkMatter.txt').record({'DMRD':spectr.ABUNDANCE[4]},spectr.NDMCROSSSECT,Number=outNumber)
            Data.In('Mass.txt').record(spectr.MASS,Number=outNumber)

            #X2_GCE=GCE(files)
            #Data.In('X2_GCE.txt').record(X2_GCE,Number=outNumber)

            # copy files
            outspectr=os.path.join(AnalysedDir,'spectr.'+str(outNumber))
            shutil.copyfile(files,outspectr)
            shutil.copyfile(files.replace('spectr','inp'),outspectr.replace('spectr','inp'))
            shutil.copyfile(files.replace('spectr','omega'),outspectr.replace('spectr','omega'))
