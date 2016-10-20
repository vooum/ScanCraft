#!/usr/bin/env python3
from read import *
from darkmatter import *
from outputfile import *

import sys,os,re,copy,shutil
print(sys.argv)

ignore=[ 'Landau Pole'
        #,'Relic density'
        ,'b -> c tau nu'
        ]
r=readSLHA(discountKeys=ignore)


if len(sys.argv)==1:
    key='mcmc'
else:
    if sys.argv[1][-1]=='/':
        key=sys.argv[1]
    else:
        key=sys.argv[1][:-1]
if len(sys.argv)==3:
    OutSteam=sys.argv[2]
else:
    OutSteam='Analysed'
if os.path.exists(OutSteam):exit('Directory '+ OutSteam +' already exist')
os.mkdir(OutSteam)
AnalysedDir=os.path.join(OutSteam,'record')
os.mkdir(AnalysedDir)


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

L_Nsd=DarkMatter('LUX2016_Nsd.txt')
L_Psd=DarkMatter('LUX2016_Psd.txt')
L_Psi=DarkMatter('LUX2016_Psi.txt')

outNumber=0
for files in spectrs:
    r.read(files)
    if r.p:
        if r.PROB: continue
        mainNNo=0
        mixV=0
        for i in range(5):
            if abs(r.Nmix[tuple([1,i+1])]) > abs(mixV):
                mixV=r.Nmix[tuple([1,i+1])]
                mainNNo=i+1
        # Constrants ==================================================================================

        #if mainNNo not in [5]:continue
        #if min(r.ExtPar['M1'],r.ExtPar['M2'],r.ExtPar['Atau'])<300. : continue 

        if abs(r.DM['csNsd'])>L_Nsd.value(r.Msp['X_N1']):continue
        if abs(r.DM['csPsd'])>L_Psd.value(r.Msp['X_N1']):continue
        if abs(r.DM['csPsi'])>L_Psi.value(r.Msp['X_N1']):continue

        # Record sample which pass all constraints=====================================================
        inNumber=re.findall(r'\d+',files)[-1]
        outNumber+=1   # reNumber
        #outNumber=int(inNumber) #keep original Number

        DMAnni=ClassifyDMAnni(r.DMAnnihilation)# DarkMatter Annihilation


        for i in DataFiles.values():i.number(str(outNumber))
        DataFiles['Allpar'].Data([r.MinPar,r.ExtPar])
        DataFiles['DM'].Data([r.DM])
        DataFiles['Mass'].Data([r.Mh,r.Msp])
        DataFiles['FT'].number('FT: '+str(r.FT))
        DataFiles['FT'].Data([])
        DataFiles['Nmix'].Data([r.Nmix])


        N2Decay=ClassifyEWino(r.DecayList[1000023])
        N3Decay=ClassifyEWino(r.DecayList[1000025])
        C1Decay=ClassifyEWino(r.DecayList[1000024])
        #print(C1Decay)
        for listi,filej in [[N2Decay,N2],[N3Decay,N3],[C1Decay,C1]]:
            S=sorted([i for i in listi.items()],key=lambda x:x[1],reverse=True)
            filej.write(str(outNumber)+'\t'+'\t'.join([str(i[0])+': '+str(i[1]) for i in S])+'\n')

        # copy files
        outspectr=os.path.join(AnalysedDir,'spectr.'+str(outNumber))
        shutil.copyfile(files,outspectr)
        shutil.copyfile(files.replace('spectr','inp'),outspectr.replace('spectr','inp'))
        shutil.copyfile(files.replace('spectr','omega'),outspectr.replace('spectr','omega'))
