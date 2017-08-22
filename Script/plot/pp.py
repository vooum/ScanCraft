#!/usr/bin/env python3
import sys,os,re,copy,shutil,numpy,pandas
sys.path.append('/home/vooum/Desktop/ScanCommando')

read_from_files=False
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
    #color_frame=pandas.DataFrame(color_list.reshape(1,color_list.shape[0]).transpose(),columns=['color'])

    data=pandas.concat([mass[1000022],darkmatter['DMRD'],darkmatter[1],darkmatter[4],X2_GCE['X2GCE'],color_list
                        ],axis=1)
    data.columns=['m_N1','relic','Psi','Nsd','X2_GCE','color']
    data.to_csv('data_for_plot.csv')
else:
    from command.analyse.ReadData import StringToIFT as STI
    data=pandas.read_csv('data_for_plot.csv',index_col=0)
    data.columns=([STI(i) for i in data.columns])


good=data[0.1197*.9<data['relic']<0.1197*1.1]