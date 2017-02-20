#!/usr/bin/env python3
from command.read import *
from command.Experiments.directdetection import *
from command.outputfile import *

import sys,os,re,copy,shutil
print(sys.argv)

ignore=[ 'Landau Pole'
        #,'relic density'
        ,'Muon magn. mom.'
        ,'b -> c tau nu'
        ]
r=readSLHA(discountKeys=ignore)


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
DataFiles={\
'Allpar':outputfile(os.path.join(OutSteam,'AllParameters')) #open(os.path.join(OutSteam,'AllParameters'),'w')
,'DM':outputfile(os.path.join(OutSteam,'DarkMatter'))
,'Mass':outputfile(os.path.join(OutSteam,'Mass'))
,'FT':outputfile(os.path.join(OutSteam,'FT'))
,'Nmix':outputfile(os.path.join(OutSteam,'Nmix'))
#,'Va':outputfile(os.path.join(OutSteam,'Vacuum'))
}#=open(os.path.join(OutSteam,'Obs'),'w')


N2=open(os.path.join(OutSteam,'N2Decay'),'w')
N3=open(os.path.join(OutSteam,'N3Decay'),'w')
C1=open(os.path.join(OutSteam,'C1Decay'),'w')
#-------------- get all spectr and omega files
spectrs=[]
#omegas=[]
record='record'
for dirs in os.listdir():
    spectr0=[]
    if key in dirs and os.path.isdir(dirs):
        for files in os.listdir(os.path.join(dirs,record)):
            #if files=='spectr.0':continue
            name=os.path.join(dirs,record,files)
            if 'spectr' in files and os.path.isfile(name) and 'from' not in files:
                spectr0.append(name)
        spectr0.sort(key=lambda x: int(re.findall(r'\d+',x)[-1]))
        spectrs.extend(spectr0)

L_Nsd=DirectDetection('LUX2016_Nsd.txt')
L_Psd=DirectDetection('LUX2016_Psd.txt')
L_Psi=DirectDetection('LUX201608_Psi.txt')

outNumber=0
for files in spectrs:
    r.read(files)
    if r.p:
        #if r.PROB: continue
        mainNNo=0
        mixV=0
        # Constrants ==================================================================================

        # Record sample which pass all constraints=====================================================
        inNumber=re.findall(r'\d+',files)[-1]
        outNumber+=1   # reNumber
        #outNumber=int(inNumber) #keep original Number

        for i in DataFiles.values():i.number(str(outNumber))
        DataFiles['Allpar'].Data([r.MinPar,r.ExtPar])
        DataFiles['DM'].Data([r.DM])
        DataFiles['Mass'].Data([r.Mh,r.Msp])
        DataFiles['FT'].number('FT: '+str(r.FT))
        DataFiles['FT'].Data([])
        DataFiles['Nmix'].Data([r.Nmix])
        Data.In('BlockMass').record(r.Mass)

        # copy files
        outspectr=os.path.join(AnalysedDir,'spectr.'+str(outNumber))
        shutil.copyfile(files,outspectr)
        shutil.copyfile(files.replace('spectr','inp'),outspectr.replace('spectr','inp'))
        shutil.copyfile(files.replace('spectr','omega'),outspectr.replace('spectr','omega'))
