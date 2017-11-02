#!/usr/bin/env python3
"""
File: testCovar.py
Author: Christoph Weniger
Email: c.weniger@uva.nl
Date: 2014-09-22
Description: Test unit for public flux covariance matrix data
"""
## modified by Yang Zhang
# To calculate the chisq of the spectrum given by micromegas
# except the primary input 'covariance.dat'

from __future__ import division
from numpy import *
#import pylab as plt
from scipy import linalg,optimize
import os
import sys,re
#
# Import data
#


cov_file=os.path.join(os.path.dirname(__file__),'covariance.dat')
# data = loadtxt('covariance.dat')
data=loadtxt(cov_file)
ebins = data[:,0:2]  # Energy bins [GeV]
# \/ prod Return the product of array elements over a given axis
# \/ eg: np.prod([[1.,2.],[3.,4.]])         = 24.0
# \/     np.prod([[1.,2.],[3.,4.]], axis=1) = array([  2.,  12.])
emeans = ebins.prod(axis=1)**0.5  # Geometric mean energy [GeV]
de = ebins[:,1] - ebins[:,0]  # Energy bin width [GeV]
flux = data[:,2]  # (Average flux)*E^2 in energy bin [GeV/cm2/s/sr]
flux_err = data[:,3]  # Flux error [GeV/cm2/s/sr]
empirical_variance = data[:,4:28]  # Only empirical component [(GeV/cm2/s/sr)^2]
full_variance = data[:,28:]  # Variance as it enters the spectral fit [(GeV/cm2/s/sr)^2]
empirical_sigma = sqrt(diagonal(empirical_variance))  # Diagonal elements
full_sigma = sqrt(diagonal(full_variance))  # Diagonal elements

#
# Perform fit
#

CONSTRUCT_VARIANCE = True
if CONSTRUCT_VARIANCE:
    # Constructed sigma
    method_error = 6e-8 * emeans**-1  # Residual method error
    c, d = meshgrid(method_error, method_error)
    Sigma = empirical_variance + diag(flux_err**2) + c*d + diag(method_error**2)
else:
    # Full sigma from program
    Sigma = full_variance
invSigma = linalg.inv(Sigma)  # Inverse matrix

###############\/### Yang Zhang ###\/#######################
#
# Definition of chi^2 function
#
def chi2(mu, mode = 'total'):
    if mode == 'stat':
        return sum((mu-flux)**2/flux_err**2)
    elif mode == 'total':
        a, b = meshgrid(mu-flux, mu-flux)
        return sum(a*b*invSigma)



def X2_GCE(flux_file,eps):
    mydata = loadtxt(flux_file)
    myE = mydata[:,0]
    myF = mydata[:,1]*eps**2
    X2_i=lambda x: chi2(myF*x)
    res=optimize.minimize_scalar(X2_i,bounds=(0.2,5),method='bounded')
    return res.fun





# def SpectrList(path):
#     spectrs=[]
#     for files in os.listdir(path):
#         name=os.path.join(path,files)
#         if 'GCE' in files and os.path.isfile(name) and 'from' not in files:
#             spectrs.append(name)
#     spectrs.sort(key=lambda x: int(re.findall(r'\d+',x)[-1]))
#     return spectrs
# #f_OUT = open("Chi2_min.dat",'w')
# #f_OUT2 = open("Chi2_J_1.dat",'w')

# #for jj in range(num_tot):
# #   if  os.path.exists('micromegas'+ss2+'/NMSSM/GCE_'+ss+'/GCE'+str(jj+1)+'.dat'): 
# #     mydata = loadtxt('micromegas'+ss2+'/NMSSM/GCE_'+ss+'/GCE'+str(jj+1)+'.dat')
# #     myE = mydata[:,0]
# #     myF = mydata[:,1]
# path=sys.argv[1]
# if os.path.isfile(path):
#     spectrs=[path]
# else:
#     spectrs=SpectrList(path)

# #record=open('X2record.txt','w')
# for spectr in spectrs:
#     # number=re.findall(r'\d+',spectr)[-1]
#     # omega=os.path.join(sys.argv[1],'Omega'+number+'.dat')
#     omega=spectr.replace('GCE_out','Omega')
#     eps=loadtxt(omega,comments=['#','BLOCK'])[1,1]
#     mydata = loadtxt(spectr)
#     myE = mydata[:,0]
#     myF = mydata[:,1]*eps**2
#     # find the min in J=(0.2~5)
#     J_min=0.2
#     J_max=5.
#     N_find = 1000
#     MinChi2= chi2(myF*J_min)
#     for ii in range(N_find):
#         J_tem = J_min+ii*(J_max-J_min)/N_find
#         CurChi2 = chi2( myF*J_tem )
#         if CurChi2<=MinChi2 :
#             MinChi2= CurChi2
#             J_find = J_tem
#     chisq_1=chi2(myF)
# #   else:
# #     MinChi2=-1
# #     J_find=0
# #     chisq_1=-1
#     print(MinChi2)
