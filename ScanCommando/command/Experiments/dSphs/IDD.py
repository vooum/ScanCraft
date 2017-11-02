#! /usr/bin/env python3

import os,sys,math,re
import numpy as np
np.seterr(divide='ignore',invalid='ignore')
from scipy.interpolate import interp1d
from scipy.integrate import quad
from scipy.optimize import minimize
from scipy.optimize import brentq

#======= get all dSphs informations
global emins,emaxs,ebin
emins=None
emaxs=None
ebin=None

dSphs_List=[ ['bootes_I'            ,18.8   ,0.22]
            ,['canes_venatici_II'   ,17.9   ,0.25]
            ,['carina'              ,18.1   ,0.23]
            ,['coma_berenices'      ,19.    ,0.25]
            ,['draco'               ,18.8   ,0.16]
            ,['fornax'              ,18.2   ,0.21]
            ,['hercules'            ,18.1   ,0.25]
            ,['leo_II'              ,17.6   ,0.18]
            ,['leo_IV'              ,17.9   ,0.28]
            ,['sculptor'            ,18.6   ,0.18]
            ,['segue_1'             ,19.5   ,0.29]
            ,['sextans'             ,18.4   ,0.27]
            ,['ursa_major_II'       ,19.3   ,0.28]
            ,['ursa_minor'          ,18.8   ,0.19]
            ,['willman_1'           ,19.1   ,0.31]
            ]
class set_dSphs:
    def __init__(self,name,lgj,lgerr):
        print('Setting dSphs datas=============')
        data_file=os.path.join(os.path.dirname(__file__),'./release-01-00-02')
        self.filename=os.path.join(data_file,'like_'+name+'.txt')
        self.lgJ=lgj
        self.lge=lgerr
        self.J=10.**lgj
        self.err=self.J*(10**lgerr-1.)
        data = np.loadtxt(self.filename)/1000.

        global emins,emaxs,ebin
        if  type(emins) is type(None):
            emins, emaxs = np.unique(data[:,0]),np.unique(data[:,1])
            ebin = np.sqrt(emins*emaxs)
            print('bins:(GeV)\n',np.column_stack((emins,emaxs)))
        elif(  np.any(emins != np.unique(data[:,0]))
            or np.any(emaxs != np.unique(data[:,1]))
            ):
                exit('wrong in emains')
        self.logLikes= data[:,3].reshape(len(emins),-1)*1e3
        self.efluxes = data[:,2].reshape(len(emins),-1)
        self.likes   = [ interp1d(f,l-l.max(),assume_sorted=False,bounds_error=False,fill_value='extrapolate')
                         for f,l in zip(self.efluxes,self.logLikes) ]
        print('-'*10+os.path.basename(self.filename)+'-'*10)
        print('-- log(Jfactor)= %.2e,\t Jfactor=%.5e\n-- log(  err  )= %.2e,\t   err  =%.5e'
            %(self.lgJ,self.J,self.lge,self.err))

#======== calculate E*flux
def eN(dn,emin,emax):
    """ Integrate a generic spectrum, multiplied by E, to get the energy flux.
    """
    edn = lambda e: e*dn(e) 
    tol = min(edn(emin),edn(emax))*1e-10

    try:
        return quad(edn,emin,emax,epsabs=tol,full_output=True)[0]
    except Exception as msg:
        if silent: print('Numerical error "%s" when calculating integral flux.' % msg)
        return np.nan

def get_eN_bins(lges,dn):
    global emins,emaxs
    lg=math.log10
    lge_min,lge_max=lges.min(),lges.max()
    #print(lge_min,lge_max)#;exit()
    enbins=[]
    for e1,e2 in zip(emins,emaxs):
        lge1,lge2=lg(e1),lg(e2)        
        #print(lge1,lge2,end='\t')
        if lge2<lge_min:
            enbins.append( 0.)
        elif lge1<lge_min<lge2<lge_max:
            enbins.append( eN(dn,10**lge_min,e2))
        elif lge_min<lge1<lge2<lge_max:
            enbins.append( eN(dn,e1,e2))
            #print(2)
        elif lge_min<lge1<lge_max<lge2:
            enbins.append( eN(dn,e1,10**lge_max))
            #print(3)
        elif lge_max<lge1:
            enbins.append(0.)
            #print(4)
    return np.array(enbins)

def like(mDM,SigmaV,eN_bins,eps=1.,c1=1.,c2=1.,c3=1.,c4=1.,c5=1.,c6=1.,c7=1.,c8=1.,c9=1.,c10=1.,c11=1.,c12=1.,c13=1.,c14=1.,c15=1.):
    global dSphs
    Cj_list={'bootes_I':c1,
    'canes_venatici_II':c2,
               'carina':c3,
       'coma_berenices':c4,
                'draco':c5,
               'fornax':c6,
             'hercules':c7,
               'leo_II':c8,
               'leo_IV':c9,
             'sculptor':c10,
              'segue_1':c11,
              'sextans':c12,
        'ursa_major_II':c13,
           'ursa_minor':c14,
            'willman_1':c15
            }
    for dwarf in dSphs.keys():
        dSphsi=dSphs[dwarf]
        dSphsi.eflux= eN_bins*abs((1./4./math.pi) * (SigmaV/2./mDM**2) * dSphsi.J * Cj_list[dwarf] * eps**2)
        dSphsi.like = sum([lnlfn(p) for lnlfn,p in zip(dSphsi.likes,dSphsi.eflux)])
        dSphsi.J_like=(Cj_list[dwarf]-1.)**2/2./(10.**dSphsi.lge-1.)**2
        #print(dwarf,dSphsi.like,dSphsi.J_like,SigmaV)
    x2=sum([abs(i.like)+abs(i.J_like) for i in dSphs.values()])
    #print(x2)
    global like_i,like_j
    like_i=sum([abs(i.like) for i in dSphs.values()])
    like_j=sum([abs(i.J_like) for i in dSphs.values()])
    return x2

# calculate X^2 of each sample
def run_sample(e_dnde,mDM,Omega,SigmaV,silent=True):
    # mDM,eps,SigmaV,e_dnde=parameters
    eps=Omega/0.1197
    energy,dnde=np.loadtxt(e_dnde,unpack=True,delimiter=',')
    log_energy = np.log10(energy)
    log_dnde = np.log10(dnde)
    #print(np.column_stack((log_energy,log_dnde)))
    log_interp = interp1d(log_energy,log_dnde,assume_sorted=False,bounds_error=False,fill_value=np.nan)
    dn = lambda e: np.nan_to_num(10**( log_interp(np.log10(e)) ))#;print(dn(10));exit()
    #eN_bins = np.array([eN(dn,e1,e2) for e1,e2 in zip(emins,emaxs)]);print(eN_bins)#;exit()
    eN_bins=get_eN_bins(log_energy,dn)
    if not silent: print('-'*20)
    #print('e*N of 25 bins:\n',eN_bins)

    f_X2_min=lambda x:like(mDM,x[0],eN_bins,eps,\
                x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15])
    f_X2_SigmaV=lambda x:like(mDM,SigmaV,eN_bins,eps,\
                x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14])

    x0_min=[1.e-26]+[1.]*15
    bounds_min=((0.,None),)+((0.5,1.5),)*15#;print(bounds_min);exit()
    x0_SV=[1.]*15
    bounds_SV=((0.5,1.5),)*15#;print(bounds_SV);exit()

    if not silent: print('sigmaV fixed and C_i=1 :\n','X2=%5.3f\tX2_rr=%5.3f\tX2_j=%3.3f'%(f_X2_SigmaV(x0_SV),like_i,like_j))

    x2min=minimize(f_X2_min,x0=x0_min,bounds=bounds_min,method='L-BFGS-B',options={'maxiter':1000000,})
    if x2min.status!=0:
        if not silent: print(x2min)#;exit('minimize err')
        return 1e10
    if not silent: print('free sigmaV and C_i :\n','X2=%5.3f\tX2_rr=%5.3f\tX2_j=%3.3f'%(x2min.fun,like_i,like_j),'\n parameters:\n',x2min.x)
    x2SV=minimize(f_X2_SigmaV,x0=x0_SV,bounds=bounds_SV,method='L-BFGS-B',options={'maxiter':1000000,})
    if x2SV.status!=0:
        if not silent: print(x2SV)#;exit('minimize err')
        return 1e10
    if not silent: print('fix sigmaV and free C_i :\n','X2=%5.3f\tX2_rr=%5.3f\tX2_j=%3.3f'%(x2SV.fun,like_i,like_j),'\n parameters:\n',x2SV.x)
    return x2SV.fun-x2min.fun

'''
=========================================================
PROGRAM BEGIN HERE
=========================================================
'''
#======== setup dSphs
global dSphs
dSphs={}
for dwarf,j,e in dSphs_List:
    dSphs[dwarf]=set_dSphs(dwarf,j,e)
print('')

def X2_dSphs(E_dNdE_file,mDM,Omega,SigmaV):# <2.71/2
    return run_sample(E_dNdE_file,mDM,Omega,SigmaV)

