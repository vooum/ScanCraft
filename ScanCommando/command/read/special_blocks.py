#! /usr/bin/env python3
from .readline import commented_out,ReadLine

class HiggsBounds_and_HiggsSingals():
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