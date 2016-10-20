#!/usr/bin/env python3
import numpy,os

class DarkMatter:
    def __init__(self,exp):
        Dir='command/darkmatter/'
        CurDir=os.getcwd()
        ExpDir={'X1TSI':'Xenon1T_SI_LXe.txt','X1TSDp':'Xenon1T_SDp.txt','X1TSDn':'Xenon1T_SDn.txt'
                ,'PICO2L_SDp.txt':'PICO2L_run2_SDp.txt','PICO60_SDp.txt':'PICO60_SDp.txt'
                ,'LUX2016_Nsd.txt':'LUX2016_Nsd.txt','LUX2016_Psd.txt':'LUX2016_Psd.txt','LUX2016_Psi.txt':'LUX2016_Psi.txt'
                ,'LUX201608_Psi.txt':'LUX201608_Psi.txt'
                }
        self.line=numpy.loadtxt(os.path.join(Dir,ExpDir[exp]))
    def value(self,mass):
        if mass<self.line[0,0]:
            return 100.
        for i in range(1,self.line.shape[0]):
            if mass < self.line[i,0]: 
                return self.line[i-1,1]+(self.line[i,1]-self.line[i-1,1])/(self.line[i,0]-self.line[i-1,0])
