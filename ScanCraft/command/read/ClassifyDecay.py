#!/usr/bin/env python3
from .readSLHA import ParticleSpectrum

def AddValue(dictionary,key,value):
    if key in dictionary.keys():
        dictionary[key]+=value
    else:
        dictionary[key]=value

def ClassifyEWino(DecayList):
    Decay={}
    #print(DecayList)
    for outS, outR in DecayList.items():
        if type(outS) is str:
            continue
        elif type(outS) is tuple:
            name=[]
            if len(outS)==2:
                if abs(outS[0]) in list(range(1000011,1000017))+list(range(2000011,2000016,2)):#SLeptons or SNeutrinos
                    if True:# Add all
                        AddValue(Decay,'SL/V&L/V',outR)
                    elif abs(outS[0])%1000000 == abs(outS[1]):# all L or V
                        if abs(outS[1])%2==1:
                            AddValue(Decay,'SL&L',outR)
                        else:
                            AddValue(Decay,'SV&V',outR)
                    elif abs( abs(outS[0])%1000000 - abs(outS[1]) ) == 1 :# one L one V
                        if outS[1]%2 == 1 :
                            AddValue(Decay,'SV&L',outR)
                        else:
                            AddValue(Decay,'SL&V',outR)
                    else:
                        print(outS)
                else:
                    for i in outS:
                        name.append(ParticleSpectrum[abs(i)])
                    Decay['&'.join(name)]=outR
            elif len(outS)==3:
                name.append(ParticleSpectrum[abs(outS[0])])
                if outS[1]+outS[2]==0:
                    name.append('Z*')
                elif abs(outS[1]+outS[2])==1:
                    name.append('W*')
                else:
                    exit('unknown decay type')
                AddValue(Decay,'&'.join(name),outR)
    return Decay

def ClassifyDMAnni(AnnihilationList):
    Anni={}
    for outS, outR in AnnihilationList.items():
        if outS[0]==outS[1]==1000022:
            AddValue(Anni,'N1N1',outR)
        else:
            AddValue(Anni,'others',outR)
    return Anni