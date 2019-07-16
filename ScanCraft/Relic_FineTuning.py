#!/usr/bin/env python3
import sys,os,re,copy,shutil,subprocess,random,math,pandas

from command.scan.scan import scan
from command.NMSSMTools import NMSSMTools
# from command.operations.getpoint import GetPoint
from command.Experiments.directdetection import DirectDetection
from command.chisqure import *
mh=[125.09, 3., 3.]
from command.format.parameter_type import *
from command.outputfile import *

from command.file_operations.GetSamples import GetSamples
from command.NMSSMTools import ReadNMSSMToolsSpectr
from command.operators.iterable import FlatToList

# settings
ism='h2'
target_number=3000
step_factor=.3 # sigma = n% of (maximum - minimum) of the free parameters
slop_factor=1. # difficulty of accepting a new point with higher chisq
ignore=[ 'Landau Pole'#27
        ,'relic density'#30
        ,'Relic density'
        ,'Excluded by LUX'
        ,'b->s gamma'#32
        ,'B_s->mu+mu-'#35
        ,'Muon magn'#37
        ,'No Higgs in the'#46
        ,'b -> c tau nu'#58 always keep alive
        ]

mold=scan()
mold.AddScalar('tanB',  'MINPAR',3, 2., 60.)
mold.AddScalar('M1',    'EXTPAR',1, 20.,800.)
mold.AddScalar('M2',    'EXTPAR',2, 100.,   1200.)
mold.AddScalar('Atop',  'EXTPAR',11,-5e3,   5e3)
mold.AddFollower('Abottom', 'EXTPAR',12,'Atop')
mold.AddScalar('Atau',      'EXTPAR',13,100.,1200.)
mold.AddFollower('MtauL',   'EXTPAR',33,'Atau')
mold.AddFollower('MtauR',   'EXTPAR',36,'Atau')
mold.AddScalar('MQ3L',  'EXTPAR',43,100.,2.e3)
mold.AddScalar('MtopR', 'EXTPAR',46,100.,2.e3)
mold.AddFollower('MbottomR','EXTPAR',49,'MtopR')
mold.AddScalar('Lambda',    'EXTPAR',61,1e-3,   .75)#,    prior_distribution='lognormal')
#mold.AddScalar('Kappa',    'EXTPAR',62,-0.75,  -1e-3,  prior_distribution='lognormal')
mold.AddScalar('minusK', 'auxiliary',62,1e-3,   .75)#,    prior_distribution='lognormal')
Minus=lambda x : -x
mold.AddDependent('Kappa',    'EXTPAR',62,func=Minus,variables=['minusK'])
mold.AddScalar('A_kappa',   'EXTPAR',64,-2.e3,2.e3)
mold.AddScalar('mu_eff',    'EXTPAR',65,100.,1000.)
mold.AddScalar('MA',        'EXTPAR',124,50.,2.e3)

par_name_list=list(mold.free_parameter_list.keys())
# set NMSSMTools
N=NMSSMTools(input_mold='./inp',
    package_dir='./NTools_Dh',
    inp_file='inp.dat',
    output_file='spectr.1.txt',
    main_routine='rerun'
    )
N.output_dir=os.path.join(N.package_dir,'out','SLHAout','spectr.1.txt')
N.output_omega_dir=N.output_dir.replace('spectr','omega')
N.output_decay_dir=N.output_dir.replace('spectr','decay')

# collect samples
samples=GetSamples(path='./diluted_good_samples',
    patterns=['inp','spectr','omega'],
)

# calculate left/right near point on every directions for each samples
for sample in samples[:200]:#636
    number_str=sample.documents['inp'].rsplit('.')[-1]
    print(number_str)

    mold.GetValue(sample.documents['inp'],mapping={'auxiliary':'EXTPAR'})
    del(mold.variable_list['Kappa'].value)
    mold.variable_list['minusK'].value=-mold.variable_list['minusK'].value
    
    diff_points={}
    # point in the central
    diff_points['central']=ReadNMSSMToolsSpectr(sample.documents['spectr'])
    
    for par in par_name_list:
        # right limit
        plus=copy.deepcopy(mold)
        plus.free_parameter_list[par].value+=plus.free_parameter_list[par].value/10000
        spectr_plus=N.Run(plus)
        destinations={
            'inp'     :os.path.join(N.record_dir,'inp.dat.'+number_str+'.'+par+'_plus'),
            'spectr'  :os.path.join(N.record_dir,'spectr.dat.'+number_str+'.'+par+'_plus'),
            'omega'   :os.path.join(N.record_dir,'omega.dat.'+number_str+'.'+par+'_plus')
        }
        shutil.copy(N.inp_dir,destinations['inp'])
        shutil.copy(N.output_dir,destinations['spectr'])
        shutil.copy(N.output_omega_dir,destinations['omega'])
        diff_points[par+'+']=spectr_plus

        # left limit
        minus=copy.deepcopy(mold)
        minus.free_parameter_list[par].value-=minus.free_parameter_list[par].value/10000
        spectr_minus=N.Run(minus)
        destinations={
            'inp'     :os.path.join(N.record_dir,'inp.dat.'+number_str+'.'+par+'_minus'),
            'spectr'  :os.path.join(N.record_dir,'spectr.dat.'+number_str+'.'+par+'_minus'),
            'omega'   :os.path.join(N.record_dir,'omega.dat.'+number_str+'.'+par+'_minus')
        }
        shutil.copy(N.inp_dir,destinations['inp'])
        shutil.copy(N.output_dir,destinations['spectr'])
        shutil.copy(N.output_omega_dir,destinations['omega'])
        diff_points[par+'-']=spectr_minus
    sample.diff_points=copy.deepcopy(diff_points)

# analyse all fine-tunings
def output_line(sample):
    diff_points=sample.diff_points
    central=diff_points['central']
    omega_0=central.ABUNDANCE[4]
    line=[
        sample.documents['inp'].rsplit('.')[-1],# number
        omega_0
    ]
    for par in par_name_list:
        block=mold.variable_list[par].block
        code=mold.variable_list[par].code
        plus=diff_points[par+'+']
        minus=diff_points[par+'-']

        pi_0=getattr(central,block)[code]
        # right limit
        omega_r=plus.ABUNDANCE[4]
        pi_r=getattr(plus,block)[code]
        Delta_r=pi_0/omega_0*abs(omega_r-omega_0)/abs(pi_0-pi_r)
        # left limit
        omega_l=minus.ABUNDANCE[4]
        pi_l=getattr(minus,block)[code]
        Delta_l=pi_0/omega_0*abs(omega_l-omega_0)/abs(pi_0-pi_l)

        line.extend([
            pi_0,omega_r,pi_r,Delta_r,omega_l,pi_l,Delta_l
        ])
    return line
column_names=['No','omega_0'].extend(
    FlatToList([
        [
            f'{par}_0',
            f'omega_{par}+',f'{par}+',f'Delta_{par}+',
            f'omega_{par}-',f'{par}-',f'Delta_{par}-'
        ]
        for par in par_name_list
    ])
)

all_ft=[
    output_line(sample)
    for sample in samples
]

Ft_pds=pandas.DataFrame(all_ft,columns=column_names)
Ft_pds.to_csv('./OmegaFineTunings')