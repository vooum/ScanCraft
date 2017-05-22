#!/usr/bin/env python3
### input './print list' to show the numbers and names of all parameters

import os,re,sys,copy
import matplotlib.pyplot as plt
import numpy as np

# functions===============================================
def input(data):
    d=[]
    for line in open(data,'r').readlines():
        c=[]
        for i in line.split('\t')[:-1]:
            c.extend(i.split(':'))
        d.append(c)
    return np.asarray(d)

class GetData:
    def __init__(self,data):
        a=input(data)
        self.name=a[0,1::2].tolist()
        self.par=a[:,2::2].astype(float)
        self.number=a[:,0].astype(int)
    def Add(self,data):
        a=input(data)
        if len(self.number)==len(a[:,0].astype(int)):
            self.name.extend(a[0,1::2].tolist())
            self.par=np.hstack((self.par,a[:,2::2].astype(float)))
        else:
            print('check the line number')
            exit()
#=========================================================

#------------------ read data file  --------------------
par=GetData('AllParameters')
par.Add('FT')
parlist=[par]   # add all parameter arrays here
if len(sys.argv)>1:
    if sys.argv[1]=='list':
        for p in parlist:
            for i in range(len(p.name)):
                print(i,p.name[i])
        exit()

#print(par.name)
#print(par.par)
#print(par.number)
# Reduce ============================================
N=300
distence=[]
delete=[True]*len(par.number)
print(len(delete))
#exit()
for i in range(len(par.name)):
    d=max(par.par[:,i])-min(par.par[:,i])
    distence.append(d)
print(len(distence))
for i in range(len(par.number)):# target line
    if delete[i]==False: continue
    for j in range(i+1,len(par.number),1):# compare line
        if delete[j]==False: continue
        for p in range(18):# compare parameter
            if distence[p]==0: continue
            if abs(par.par[i,p]-par.par[j,p])>distence[p]/N:# far
                break
        else:# two points are too near
            delete[j]=False
delete=np.array(delete)
parameter=par.par[delete]
number=par.number[delete]
print(delete)
print(len(number))

Dh=np.loadtxt('fine_tuning_Mh.txt')[delete][:,0]
'''print(Dh)
print(len(Dh))
print(parameter[:,18][:])
print(np.shape(Dh),np.shape(parameter[:,18]))'''
# Plot ===================================================
plt.figure(figsize=(12,8))
D50=((parameter[:,18]<50.) & (Dh[:]<50.))
plt.scatter(parameter[D50][:,18],Dh[D50],edgecolors='None',c=parameter[D50][:,17],vmax=400,vmin=150)
cb=plt.colorbar(extend='both')
cb.set_label('$\mu$',fontsize=24)
plt.xlim(0,50)
plt.ylim(0,50)
plt.xlabel('$\Delta_Z$',fontsize=24)
plt.ylabel('$\Delta_h$',fontsize=24)
plt.text(1,43,'SM like higgs: $h_2$ \nDM: higgsino dominated',fontsize=24,bbox={'facecolor':'white', 'alpha':1,})
plt.text(30,5,'After LUX-2016',fontsize=24)
plt.savefig('h_Ft_2')



# annihilation ==========================================
limit=list([i.split()[1] for i in open('kind','r').readlines()])
limit=np.array(limit).astype(int)[delete]
print(len(limit))
color=[]
for i in limit:
    if i < 9: color.append('r')
    elif i < 99: color.append('b')
    elif i < 999: color.append('k') 
color=np.array(color)
labels={'r':'Resonance'
        ,'b':'Large mixing'
        ,'k':'Coannihilation'}
markerlist={'k':'.','b':'x','r':'*'}
plt.figure(figsize=(10,8))
for i in ['b']:
    c=(color==i)
    plt.scatter(parameter[c & D50][:,16],abs(parameter[c & D50][:,15]),s=40,c=color[c & D50][:],marker=markerlist[i],edgecolors='face',label=labels[i])
plt.xlim(0,.7)
plt.ylim(0,.6)
#L=plt.legend(loc=4)
#colormap=map(lambda x,y: [x,y], L.get_texts() ,['b'])
#for x,y in colormap:
#    x.set_color(y)
plt.xlabel('$\lambda$',fontsize=24)
plt.ylabel('$\kappa$',fontsize=24)
plt.text(0.014,0.516,'SM like higgs: $h_2$ \nDM: higgsino dominated',fontsize=24,bbox={'facecolor':'white', 'alpha':1,})
plt.savefig('h_l_k')