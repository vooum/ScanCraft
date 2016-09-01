#!/usr/bin/env python3
from command import *
import subprocess,random,math,shutil
#print([ i for i in globals().keys() if '__' not in i])


# settings
ism='M_h2'
target=5
StepFactor=1. # sigma = n% of (maximum - minimum) of the free parameters
SlopFactor=.3 # difficulty of accepting a new point with higher chisq
add_chisq=True

#print(read.readline.readline)
#print(mcmc.Scan)

free=mcmc.Scan()
#free.add(name,block,PDG,min,max,walk='flat',step=None,value=None)
free.add('tanB','MINPAR',3,2.,60.,step=None)
free.add('M1','EXTPAR',1  ,20.    ,1000.,step=None)
free.add('M2'	,'EXTPAR'   ,2  ,100.    ,2000.,step=None)
free.add('Atop'	,'EXTPAR'   ,11  ,  -6e3    ,6e3,step=None)
free.add('Abottom','EXTPAR'   ,12,-6e3,6e3,walk=free.Atop)
free.add('Atau'	,'EXTPAR'   ,13  ,  100.      ,2000.,step=None)
free.add('MtauL','EXTPAR'   ,33,	100.,	2.e3,walk=free.Atau)
free.add('MtauR','EXTPAR'   ,36,	100.,	2.e3,walk=free.Atau)
free.add('MQ3L'	,'EXTPAR'   ,43,	100.,	2.e3,step=None)
free.add('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3,step=None)
free.add('MbottomL','EXTPAR'  ,49,	100.,	2.e3 ,walk=free.MtopR)
free.add('lambda','EXTPAR'  ,61  ,1e-3    ,1. ,walk='log',step=None)
free.add('kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,walk='log',step=None)
free.add('A_kappa','EXTPAR' ,64,-3.e3,3.e3,step=None)
free.add('mu_eff','EXTPAR'  ,65,100.,1500.,step=None)
free.add('MA','EXTPAR',124,	0.,	2.e3)
'''print(free.tanB.max)
print(getattr(free,'tanB',None).walk)
print(free.list)
print(free.tanB.value)
free.GetNewPoint()
print(free.tanB.new_value)'''

# read start points================================
inpModel=open(inpModelDir,'r')
inpModelLines=inpModel.readlines()
inpModel.close()
if True:
    BLOCK=''
    for line in inpModelLines:
        a=readline(line)
        if a[-1] and a[0]=='BLOCK':
            BLOCK=a[1]
        else:
            if hasattr(free,BLOCK):
                P=getattr(free,BLOCK)
                if a[0] in P.keys():
                    P[a[0]].value=a[1]

free.SetRandom()
exit()
'''for i in free.list:
    print(getattr(free,i).value,end='\t')
    print()
free.GetNewPoint()
for i in free.list:
    print(getattr(free,i).new_value,end='\t')
    print()'''

L_Nsd=DarkMatter('LUX2016_Nsd.txt')
L_Psd=DarkMatter('LUX2016_Psd.txt')
L_Psi=DarkMatter('LUX2016_Psi.txt')

record=-1
trypoint=0
lastchisq=1e10
while record < target:
    if trypoint%100==1: print(trypoint,' points tried; ',record,' points recorded')
    trypoint+=1
# rewrite inp-------------------------------------------------------
    inp=open(inpDir,'w')
    BLOCK = ''
    Nnewline=0
    for line in inpModelLines:
        newline=''
        a=readline(line)
        if a[0]=='BLOCK':
            BLOCK = a[1]
        else:
            if hasattr(free,BLOCK):
                P=getattr(free,BLOCK)
                if a[0] in P.keys():
                    i=P[a[0]]
                    newline='\t'+'\t'.join([str(i.PDG),str(i.new_value),a[-2]])+'\n'
        if newline == '':		#output mcmcinp
      	    inp.write(line)
        else:   #inp.write('#--- original line'+line)
            inp.write(newline)
    inp.close()

#--------- run nmhdecay.f ----------------------
    f1=open('err.log','w')
    nmhdecay =  subprocess.Popen(run
  	    ,stderr=f1, stdout=f1, cwd=NMSSMToolsDir, shell=True).wait()

#--------- read output ------------------------
    if not os.path.exists(spectrDir): exit('spectr.dat not exist')
    if r.readfile(spectrDir):
        mainNNo=0
        mixV=0
        for i in range(5):
            if abs(r.Nmix[tuple([1,i+1])]) > abs(mixV):
                mixV=r.Nmix[tuple([1,i+1])]
                mainNNo=i+1
        
        #if mainNNo not in [5]:continue
        if abs(r.DM['csNsd'])>L_Nsd.value(r.Msp['X_N1']):continue
        if abs(r.DM['csPsd'])>L_Psd.value(r.Msp['X_N1']):continue
        if abs(r.DM['csPsi'])>L_Psi.value(r.Msp['X_N1']):continue
        chisq=0.
        chisq_Q={}
        chisq_A={}
        chisq_A['FT']=(max(r.FT[sorted(r.FT.keys())[-2]],40.)-40.)**2/100.
        for i in chisq_Q.values():
            chisq+=i
        if add_chisq :
            for i in chisq_A.values(): 
                chisq+=i
#   record point
        if (random.random() < math.exp(max(SlopFactor*min(lastchisq-chisq,0.),-745))
    	    or chisq<10.):
            lastchisq=chisq
            free.record()
            print(record,'points recorded.')
            print('\nnew point accepted: -------------------')
            print('x2=  ',chisq,'\nx2_i= ',chisq_Q,chisq_A)
            print('Higgs masses: ',r.Mh)
            free.print()

            record+=1
            shutil.copyfile(inpDir,os.path.join(recordDir,'inp.'+str(record)))
            shutil.move(spectrDir,os.path.join(recordDir,'spectr.'+str(record)))
            shutil.move(omegaDir,os.path.join(recordDir,'omega.'+str(record)))

    free.GetNewPoint()