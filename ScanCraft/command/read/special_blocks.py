#! /usr/bin/env python3
from .readline import commented_out,ReadLine

'''
including:
    HiggsBoundsInputHiggsCouplingsBosons
    Annihilation
'''

class special_blocks():
    def HIGGSBOUNDSINPUTHIGGSCOUPLINGSBOSONS(text):
        eff_C={}        
        while True:
            try:
                line=text.NextLine()
            except IndexError:
                break
            else:
                if commented_out(line):
                    continue
                semanteme=ReadLine(line)

                try:
                    v=semanteme[0]
                except IndexError:
                    continue

                if str(v).upper()=='BLOCK':
                    break

                np=int(semanteme[1])
                tuple_p=tuple([int(i) for i in semanteme[2:2+np]])
                eff_C.update({tuple_p:v})
        return eff_C

    def HIGGSBOUNDSINPUTHIGGSCOUPLINGSFERMIONS(text):
        eff_C={}
        while True:
            try:
                line=text.NextLine()
            except IndexError:
                break
            else:
                if commented_out(line):
                    continue
                semanteme=ReadLine(line)

                try:
                    v=max(semanteme[:2])
                except IndexError:
                    continue

                if str(semanteme[0]).upper()=='BLOCK':
                    break

                np=int(semanteme[2])
                tuple_p=tuple([int(i) for i in semanteme[3:3+np]])
                eff_C.update({tuple_p:v})
        return eff_C

    def HIGGSBOUNDSRESULTS(text):
        HBresult={}
        while True:
            try:
                line=text.NextLine()
            except IndexError:
                break
            else:
                if commented_out(line):
                    continue
                semanteme=ReadLine(line)

                if str(semanteme[0]).upper()=='BLOCK':
                    break
                
                if semanteme[1]==1:
                    HBresult['channel'+str(int(semanteme[0]))]=int(semanteme[2])
                elif semanteme[1]==2:
                    HBresult['HBresult'+str(int(semanteme[0]))]=int(semanteme[2])
                elif semanteme[1]==3:
                    HBresult['obsratio'+str(int(semanteme[0]))]=semanteme[2]
        return HBresult

    def HIGGSSIGNALSRESULTS(text):
        HSresult={}
        while True:
            try:
                line=text.NextLine()
            except IndexError:
                break
            else:
                if commented_out(line):
                    continue
                semanteme=ReadLine(line)

                if str(semanteme[0]).upper()=='BLOCK':
                    break

                if semanteme[0]==13:
                    HSresult['Probability']=semanteme[1]
                elif semanteme[0]==12:
                    HSresult['X2_total']=semanteme[1]
        return HSresult


    def ANNIHILATION(text):
        anni={}
        while True:
            try:
                line=text.NextLine()
            except IndexError:
                break
            else:
                if commented_out(line):
                    continue
                semanteme=ReadLine(line)

                try:
                    No=semanteme[0]
                except IndexError:
                    continue

                if str(No).upper()=='BLOCK':
                    break

                if No==0.:
                    anni['SigmaV']=semanteme[1]
                else:
                    anni[' '.join(semanteme[2:])]=semanteme[1]
        return anni

# class general_blocks():
#     def 