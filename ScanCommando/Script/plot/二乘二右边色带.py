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
par.Add('DarkMatter')
par.Add('Mass')
RC_h=GetData('Higgs_Reduced_Couplings')
#par.Add('gghrr')
parlist=[par,RC_h]   # add all parameter arrays here
if len(sys.argv)>1:
    #if eval(sys.argv[1]).
    if sys.argv[1]=='list':
        for p in parlist:
            for i in range(len(p.name)):
                print(i,p.name[i])
        exit()

#print(par.name)
#print(par.par)
#print(par.number)
# Reduce ============================================
gghrr=np.loadtxt('CSgghrr.txt')

eps=par.par[:,19]/0.1197
#plt.semilogy()
#x,y,c=16,17,0
xyz0=np.column_stack((gghrr,eps,RC_h.par[:,6:12]))#,RC_h.par[:,6],RC_h.par[:,6],RC_h.par[:,6],RC_h.par[:,6],RC_h.par[:,6]))
                                    #h2- 2u ,3d,4b,5v,6g,7r
labels={2:'$C_{u}$',3:'$C_{d}$',4:'$C_{b}$',5:'$C_{V}$',6:'$C_{gg}$',7:'$C_{\gamma\gamma}$'}

xyz_g=xyz0[np.argsort(xyz0[:,0])]
#xyz_D=xyz0[np.argsort(xyz0[:,3])]

fig=plt.figure(figsize=(10,8))

#--------------------------------------- CV/Cr
#images=[]
#ax=[]
for n,ij in enumerate([[7,5],[6,5],[2,5],[4,5]]):
    i,j=ij[0],ij[1]
    ni=n%2
    nj=n//2
    pos=[0.1+ni*0.43,0.1+nj*0.45,0.35,0.35]
    a=fig.add_axes(pos)
    color=a.scatter(xyz_g[:,i],xyz_g[:,j],6,
                c=xyz_g[:,0],edgecolors='face')
    plt.xlabel(labels[i],fontsize=20)
    plt.ylabel(labels[j],fontsize=20)
    plt.xlim(0.9,1.1)
    plt.ylim(0.9,1.1)

#images.append(t)
#ax.append(a)
#images[0].set_norm()

#plt.axes(ax[0])
#plt.sci(images[0])

#--------------------------------------- color bar
cax = fig.add_axes([0.9, 0.1, 0.025, 0.8])
cb=fig.colorbar(color,cax)
cb.set_label(r'$\sigma_{gg \rightarrow rr}(fb)$',fontsize=24)






plt.savefig('ReducedCouplings_hsm',dpi=300)
exit()
