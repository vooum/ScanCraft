#!/usr/bin/env python3
import sys,os,re,copy,shutil,numpy,pandas
sys.path.append('/home/heyangle/Desktop/ScanCommando/ScanCommando')
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

read_from_files=False
read_from_files=True

if read_from_files:
    from command.analyse.ReadData import standard_form_data as sfd
    read=sfd.ReadStandardData
    N1Decay=read('N1_annihilation.txt').fillna(0.)
    all_par=read('AllParameters.txt')
    darkmatter=read('DarkMatter.txt')
    mass=read('Mass.txt')
    X2_GCE=pandas.DataFrame(numpy.loadtxt('X2_GCE.txt',usecols=(1)),columns=['X2GCE'])
    #print(N1Decay)
    final_states=N1Decay.iloc[:,1:].idxmax(axis=1)
    color_list=pandas.DataFrame(numpy.where(final_states==(5,-5),'b','k'))
    br_bb=N1Decay[(5,-5)]
    br_ll=N1Decay[(15,-15)]
    br_uu=N1Decay[(4,-4)]
    #color_frame=pandas.DataFrame(color_list.reshape(1,color_list.shape[0]).transpose(),columns=['color'])

    DM=pandas.concat([mass[1000022],darkmatter['DMRD'],darkmatter[1],darkmatter[4],X2_GCE['X2GCE'],N1Decay[(0,0)],br_uu,br_bb,br_ll,color_list],axis=1)
    DM.columns=['m_N1','relic','Psi','Nsd','X2_GCE','SigmaV','br_uu','br_bb','br_ll','color']

    IDD=pandas.DataFrame(numpy.loadtxt('indirect_X2.txt'))
    IDD.columns=['X2_GCE','X2_dSphs']

    LSP=read('LSP.txt').loc[:,[3,4,5]]
    LSP.columns=['N13','N14','N15']
    
    Par=pandas.concat([
        read('MINPAR')[3],
        read('EXTPAR').loc[:,[1,2,61,62,65]]
        ],axis=1)
    Par.columns=['tanB','M1','M2','Lambda','Kappa','mu']

    HiggsMass=mass.loc[:,[25,35,45,36,46]]
    HiggsMass.columns=['m_'+i for i in ['h1','h2','h3','A1','A2']]

    data=pandas.concat([DM,LSP,Par,HiggsMass,IDD],axis=1)
    good=data.query('0.1197*.9<relic<0.1197*1.1 & X2_GCE<35.2')

    data.to_csv('data_for_plot.csv')
    good.to_csv('good_for_plot.csv')
else:
    from command.analyse.ReadData import StringToIFT as STI
    data=pandas.read_csv('data_for_plot.csv',index_col=0)
    data.columns=([STI(i) for i in data.columns])
    good=pandas.read_csv('good_for_plot.csv',index_col=0)
    good.columns=([STI(i) for i in good.columns])

Xenon1T=numpy.loadtxt('Xenon1T_2017.txt')
PdX_Nsd=numpy.loadtxt('PandaX_Nsd_2016.txt')


# good=data.query('0.1197*.9<relic<0.1197*1.1 & X2_GCE<35.2')

def GCE_m_SigmaV():
    logSV=numpy.log10(good.SigmaV)
    ticks_list=numpy.log10([i*1e-27 for i in range(3,10)]+[i*1e-26 for i in range(1,6)])
    ticklabels_list=['$%iE-27$'%i for i in range(3,10)]+['$%iE-26$'%i for i in range(1,6)]

    plt.figure(figsize=(7.5,6))
    plt.scatter(good.m_N1,good.X2_GCE,10,c=logSV,cmap=plt.get_cmap('hsv'))
    cb=plt.colorbar(ticks=ticks_list)
    cb.set_ticklabels(ticklabels_list)
    cb.set_label(r'$\langle\sigma v\rangle_0\ \mathrm{(cm^3/s)}$',fontsize=15)
    plt.xlabel(r'$m_{\widetilde{\chi}^0_1}$ (GeV)',fontsize=15)
    plt.ylabel(r'$\chi^2_{GCE}$',fontsize=15)
    plt.savefig('GCE_m_SigmaV',dpi=200)

def Nsd_Psi_GCE():
    Xenon_mi=interp1d(Xenon1T[:,0],Xenon1T[:,1]*1e-45)
    PdX_mi=interp1d(PdX_Nsd[:,0],PdX_Nsd[:,1])
    X1T=Xenon_mi(good.m_N1.max())
    PdX=PdX_mi(good.m_N1.max())
    print(X1T,PdX)
    plt.figure(figsize=(7.5,6))
    plt.loglog()
    plt.plot([X1T,X1T],[1e-41,1e-38],c='darkblue')
    plt.text(X1T,1e-40,'Xenon1T',rotation=90,color='darkblue',ha='center',backgroundcolor='w')
    plt.plot([1e-53,1e-43],[PdX,PdX],c='darkred')
    plt.text(1e-49,PdX,'PandaX-II',color='darkred',va='center',backgroundcolor='w')
    plt.xlim(8e-52,3e-44)
    plt.ylim(4e-41,2e-39)
    plt.scatter(good.Psi,abs(good.Nsd),10,c=good.X2_GCE)
    cb=plt.colorbar()
    cb.set_label(r'$\chi^2_{GCE}$',fontsize=15)
    plt.xlabel(r'$\sigma^{SI}_{P{-}\chi}\ \rm{(cm^2)}$',fontsize=15)
    plt.ylabel(r'$\sigma^{SD}_{N{-}\chi}\ \rm{(cm^2)}$',fontsize=15)
    plt.savefig('Nsd_Psi_GCE',dpi=200)

def mA1_mN1_GCE():
    plt.figure(figsize=(7.5,6))
    plt.scatter(good.m_N1,good.m_A1,10,c=good.X2_GCE)
    cb=plt.colorbar()
    cb.set_label(r'$\chi^2_{GCE}$',fontsize=15)
    plt.plot([60,80],[120,160],color='darkblue')
    plt.text(64,134,r'$m_{A_1}/m_{\widetilde{\chi}^0_1}=2$',rotation=42,fontsize=15,color='darkblue')
    plt.xlim(60,71)
    plt.ylim(114,140)
    plt.xlabel(r'$m_{\widetilde{\chi}^0_1}$ (GeV)',fontsize=15)
    plt.ylabel(r'$m_{A_1}$ (GeV)',fontsize=15)
    plt.savefig('mA1_mN1_GCE',dpi=200)

# GCE_m_SigmaV()
# Nsd_Psi_GCE()
# mA1_mN1_GCE()

#===========================
# def Psi_m_SigmaV():
#     logSV=numpy.log10(good.SigmaV)
#     ticks_list=numpy.log10([i*1e-27 for i in range(3,10)]+[i*1e-26 for i in range(1,6)])
#     ticklabels_list=['$%iE-27$'%i for i in range(3,10)]+['$%iE-26$'%i for i in range(1,6)]

#     plt.figure(figsize=(7.5,6))
#     plt.semilogy(Xenon1T[:,0],Xenon1T[:,1]*1e-45,c='g')
#     plt.scatter(good.m_N1,good.Psi,5,c=logSV)
#     cb=plt.colorbar(ticks=ticks_list)
#     cb.set_ticklabels(ticklabels_list)
#     cb.set_label(r'$\sigma v\ \mathrm{(cm^3/s)}$',fontsize=15)
#     plt.xlim(60,75)
#     plt.savefig('Psi_m_SigmaV',dpi=200)

# def Nsd_m():
#     plt.figure(figsize=(7.5,6))
#     plt.semilogy()
#     plt.scatter(good.m_N1,abs(good.Nsd))
#     plt.savefig('Nsd_m',dpi=200)
# Nsd_m()

# def Sigma_GCE_m():
#     plt.figure(figsize=(7.5,6))
#     plt.semilogy()
#     plt.scatter(good.X2_GCE,good.SigmaV,c=good.m_N1)
#     plt.savefig('Sigma_GCE_m',dpi=200)

# def LSP():
#     plt.figure(figsize=(7.5,6))
#     plt.scatter(good.N13**2+good.N14**2,good.X2_GCE)
#     plt.savefig('LSP')
# LSP()

# def L_K():
#     plt.figure(figsize=(7.5,6))
#     plt.scatter(good.Lambda,good.Kappa)
#     plt.savefig('Lambda_Kappa',dpi=200)
# L_K()
    
# def mu_L():
#     plt.figure(figsize=(7.5,6))
#     plt.scatter(good.Lambda,good.mu)
#     plt.savefig('mu_Lambda',dpi=200)
# mu_L()
    
# def mu_K():
#     plt.figure(figsize=(7.5,6))
#     plt.scatter(good.Kappa,good.mu)
#     plt.savefig('mu_Kappa',dpi=200)
# mu_K()

# def br_uull_bb_SigmaV():
#     logSV=numpy.log10(good.SigmaV)
#     ticks_list=numpy.log10([i*1e-27 for i in range(3,10)]+[i*1e-26 for i in range(1,6)])
#     ticklabels_list=['$%iE-27$'%i for i in range(3,10)]+['$%iE-26$'%i for i in range(1,6)]

#     plt.figure(figsize=(7.5,6))
#     plt.scatter(good.br_bb,good.br_ll+good.br_uu,10,c=logSV,cmap=plt.get_cmap('hsv'))
#     cb=plt.colorbar(ticks=ticks_list)
#     cb.set_ticklabels(ticklabels_list)
#     cb.set_label(r'$\langle\sigma v\rangle_0\ \mathrm{(cm^3/s)}$',fontsize=15)
#     plt.xlim(0.86,0.91)
#     plt.ylim(0.09,0.14)
#     plt.plot([0,1],[1,0])
#     plt.xlabel(r'$Br(b\bar{b})$',fontsize=15)
#     plt.ylabel(r'$Br(l\bar{l})+Br(u\bar{u})$',fontsize=15)    
#     plt.savefig('br_uull_bb_SigmaV',dpi=200)
# br_uull_bb_SigmaV()

# def br_uull_bb_GCE():
#     logSV=numpy.log10(good.SigmaV)
#     ticks_list=numpy.log10([i*1e-27 for i in range(3,10)]+[i*1e-26 for i in range(1,6)])
#     ticklabels_list=['$%iE-27$'%i for i in range(3,10)]+['$%iE-26$'%i for i in range(1,6)]

#     plt.figure(figsize=(7.5,6))
#     plt.scatter(good.br_bb,good.br_ll+good.br_uu,10,c=good.X2_GCE)
#     cb=plt.colorbar()
#     cb.set_label(r'$\chi^2_{GCE}$',fontsize=15)
#     plt.xlim(0.86,0.91)
#     plt.ylim(0.09,0.14)
#     plt.plot([0,1],[1,0])
#     plt.xlabel(r'$Br(b\bar{b})$',fontsize=15)
#     plt.ylabel(r'$Br(l\bar{l})+Br(u\bar{u})$',fontsize=15)    
#     plt.savefig('br_uull_bb_GCE',dpi=200)
# br_uull_bb_GCE()

# def A1_GCE():
#     plt.figure(figsize=(7.5,6))
#     plt.scatter(good.X2_GCE,good.br_bb+good.br_ll+good.br_uu,10)    
#     plt.savefig('A1_GCE',dpi=200)
# A1_GCE()

# def OMG_SigmaV():
#     logSV=numpy.log10(good.SigmaV)
#     ticks_list=numpy.log10([i*1e-27 for i in range(3,10)]+[i*1e-26 for i in range(1,6)])
#     ticklabels_list=['$%iE-27$'%i for i in range(3,10)]+['$%iE-26$'%i for i in range(1,6)]

#     plt.figure(figsize=(7.5,6))
#     plt.semilogx()
#     plt.scatter(good.SigmaV,good.relic,c=logSV,cmap=plt.get_cmap('hsv'))
#     plt.savefig('OMG_SigmaV',dpi=200)
# OMG_SigmaV()