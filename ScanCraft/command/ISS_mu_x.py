#!/usr/bin/env python3
'''
Function: mu_x parameterization in order to compare with neutrino data
Authour: Guo xiaofei and Yue yuanfang  
time: 2018.2.4
Refrence: 
    Arxiv: 1612.06403, 1707.09626 
    mu_x paramerization leading order: eq.2.11
    mu_x next order parametrization: 2.12
Notes:
in.txt:
    ES_Yv_11 ES_Yv_22 ES_Yv_33 ES_LAMN_11 ES_LAMN_22 ES_LAMN_33

   M_D=vu/sqrt(2) * Y_v
   M_R=vs/sqrt(2) * lambda_N
 
Functionalized by He Yangle @ 2018.07.20
'''
from math import *
import numpy as np
def GetMuX(*data):
    # input: ES_Yv_11, ES_Yv_22, ES_Yv_33, ES_LAMN_11, ES_LAMN_22, ES_LAMN_33, tanbeta, vs
    tanbeta=data[6]
    # print('tanbeta=',tanbeta)

    v=246.0
    vu=v*sin(atan(tanbeta))
    vd=v*cos(atan(tanbeta))

    MD_1=vu*data[0]/sqrt(2.)
    MD_2=vu*data[1]/sqrt(2.)
    MD_3=vu*(data[2])/sqrt(2.)

    MD_dia=[MD_1,MD_2,MD_3]
    MD=np.mat(np.diag(MD_dia))
    MD_T=MD.T

    # print('MD \n', MD)
    # print('MD.T \n',MD.T)

    vs=data[7]
    MR_1=vs*data[3]/sqrt(2.)
    MR_2=vs*data[4]/sqrt(2.)
    MR_3=vs*data[5]/sqrt(2.)

    MR_dia=[MR_1,MR_2,MR_3]
    MR=np.mat(np.diag(MR_dia))
    MR_T=MR.T
    # print (MR and MR_T \n", MR,MR_T)

    U_pmns=np.mat([[0.82, 0.54, -0.15],[-0.35, 0.7, 0.62],[0.44, -0.45, 0.77]])
    U_pmns_T=U_pmns.T

    # print("U_pmns and U_pmns_T \n",  U_pmns,U_pmns_T)

    # for normal ordering...
    m1_no=0.1E-09
    deltam21_no=7.5E-23
    deltam31_no=2.524E-21
    m2_no=sqrt(m1_no**2+deltam21_no)
    m3_no=sqrt(m1_no**2+deltam31_no)
    m_no_dia=[m1_no,m2_no,m3_no]
    mass_no=np.mat(np.diag(m_no_dia))
    # print('mass_no=\n',mass_no)

    #Arxiv: 1612.06403: eq 2.11 
    #    Leading normal order mu_x paramerization; 
    # mu_x_no=MR_T.dot(linalg.inv(MD_T)).dot(U_pmns).dot(mass_no).dot(U_pmns_T).dot(linalg.inv(MD)).dot(MR)

    #Arxiv: 1612.06403
    # Next order normal order. eq 2.12

    # Note that MR,MD,U_pmns are real matrix
    # Neutrino normal order used 
    part1=np.linalg.inv(np.eye(3)-1/2.0 * np.eye(3).dot(MR.I).dot(MD).dot(MR.T.I))
    part2=MR.T.dot(MD.I).dot(U_pmns).dot(mass_no).dot(U_pmns.T).dot((MD.T).I).dot(MR)
    part3=np.linalg.inv(np.eye(3)-1/2.0 * np.eye(3).dot(MR.I).dot(MD).dot(MR.T.I))
    mu_x_no=part1.dot(part2).dot(part3)
    # print('mu_x=\n',mu_x_no)

    # 2018.2.12
    # set mu_x=0
    # mu_x_no=np.zeros((3,3))

    return mu_x_no

# for inverted ordering...
#m1_io=0.1E-9
#deltam21_io=7.5E-23
#deltam31_io=-2.524E-21
#m2_io=sqrt(m1_no**2+deltam21_io)
#m3_io=sqrt(m1_no**2+deltam31_io)
#m_io_dia=[m1_io,m2_io,m3_io]
#mass_io=mat(diag(m_io_dia))

#print "validate..." 
#print mass_no
#print mass_io

#mu_x_io=((((((MR_T.dot(linalg.inv(MD_T))).dot(U_pmns)).dot(mass_io)).dot(U_pmns_T)).dot(linalg.inv(MD))).dot(MR))
#print mu_x_io

#savetxt('out.txt',mu_x_io,delimiter=' ')


# for unitarity

#eta=0.5*MD_T.dot(linalg.inv(MR_T)).dot(linalg.inv(MR)).dot(MD)
#print eta
#savetxt('out2.txt',eta,delimiter=' ')

#os.system('cat out1.txt out2.txt > out.txt')
#print MD_T,linalg.inv(MR_T),linalg.inv(MR),MD, MD_T.dot(linalg.inv(MR_T)),MD_T.dot(linalg.inv(MR_T)).dot(linalg.inv(MR)),MD_T.dot(linalg.inv(MR_T)).dot(linalg.inv(MR)).dot(MD)