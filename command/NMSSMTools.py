#!/usr/bin/env python3
import os,shutil,subprocess,copy
from .read import *

def _GetDefaultDir():
    NMSSMToolsDir=''
    for i in os.listdir():
        if 'NMSSMTools' in i and os.path.isdir(i):
            NMSSMToolsDir=max(NMSSMToolsDir,i)
    else:
        if NMSSMToolsDir=='':
            exit('no NMSSMTools package found')
    return NMSSMToolsDir

def GetContent(FileDir):
    File=open(FileDir,'r')
    FileLines=File.readlines()
    File.close()
    return FileLines

class NMSSMTools():
    def __init__(self,Dir=_GetDefaultDir(),DataDir='mcmc/'):
        if Dir not in os.listdir(): # creat new NMSSMTools copy
            Package=_GetDefaultDir()
            subprocess.Popen('make clean', cwd=Package, shell=True).wait()            
            shutil.copytree(Package,Dir)

        self.Dir=Dir
        self.inpModelLines=GetContent(os.path.join(DataDir,'inp.dat'))
        self.inpDir=os.path.join(Dir,'mcmcinp.dat')
        self.spectrDir=self.inpDir.replace('inp','spectr')
        self.omegaDir=self.inpDir.replace('inp','omega')
        self.recordDir=os.path.join(DataDir,'record/')
        self.runcode='./run mcmcinp.dat'

        if os.path.exists(self.recordDir):
            if input('clean record? y/n \n') in ['n','N']:
                exit('Directory record/ is not deleted')
            else:
                shutil.rmtree(self.recordDir)
        os.mkdir(self.recordDir)

        if not os.path.exists(os.path.join(Dir,'main/nmhdecay')):
            subprocess.Popen('make init', cwd=Dir, shell=True).wait()
            subprocess.Popen('make', cwd=Dir, shell=True).wait()
        else: print(os.path.join(Dir,'main/nmhdecay'),'exist')

    def run(self,point,attr='new_value',ignore=[]):
        #write inp file
        inp=open(self.inpDir,'w')
        BLOCK=''
        for line in self.inpModelLines:
            newline=''
            a=readline(line)
            if a[0]=='BLOCK':
                BLOCK=a[1]
            else:
                if hasattr(point,BLOCK):
                    P=getattr(point,BLOCK)
                    if a[0] in P.keys():
                        i=P[a[0]]
                        newline='\t'+'\t'.join([str(i.PDG),str(getattr(i,attr)),a[-2]])+'\n'
            if newline == '':		#output mcmcinp
                inp.write(line)
            else:   #inp.write('#--- original line'+line)
                inp.write(newline)
        inp.close()
        #run NMSSMTools
        f1=open('err.log','w')
        subprocess.Popen(self.runcode
  	    ,stderr=f1, stdout=f1, cwd=self.Dir, shell=True).wait()
        
        if not os.path.exists(self.spectrDir): exit('spectr.dat not exist')

        result=readSLHA(discountKeys=ignore)
        result.read(self.spectrDir)
        return copy.deepcopy(result)

    def record(self,number):
        recordinp   =os.path.join(self.recordDir,'inp.'+str(number))
        recordspectr=os.path.join(self.recordDir,'spectr.'+str(number))
        recordomega =os.path.join(self.recordDir,'omega.'+str(number))
        shutil.move(self.inpDir,recordinp)
        shutil.move(self.spectrDir,recordspectr)
        if os.path.isfile(self.omegaDir):
            shutil.move(self.omegaDir,recordomega)