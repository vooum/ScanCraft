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

                if No==0:
                    anni['SigmaV']=semanteme[1]
                else:
                    anni[' '.join(semanteme[2:])]=semanteme[1]
        return anni