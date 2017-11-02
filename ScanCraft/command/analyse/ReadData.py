#!/usr/bin/env python3
import numpy,pandas
from pandas.core.frame import DataFrame

def StringToIFT(string):#translate string to int/float/tuple
    try:# translate name
        trans=eval(string)
    except NameError:# can not translate string
        trans=string
    except SyntaxError:
        trans=string
    else:
        if type(trans) not in [int,float,tuple]:# unexcepted translate
            trans=string
    return trans

block_code_name={}
block_code_name['MASS']={
    1:'d',2:'u',3:'s',4:'c',5:'b',6:'t',
    11:'e-',12:'nu_e',13:'muon',14:'nu_mu',15:'tau',16:'nu_tau',
    21:'gluon',22:'r',23:'Z',24:'W',
    25:'h1',35:'h2',36:'A1',37:'C1',45:'h3',46:'A2',
    1000001:'Sd_L',1000002:'Su_L',1000003:'Ss_L',1000004:'Sc_L',1000005:'Sb_1',1000006:'St_1',
    2000001:'Sd_R',2000002:'Su_R',2000003:'Ss_R',2000004:'Sc_R',2000005:'Sb_2',2000006:'St_2',
	1000011:'Se_L',1000012:'Snu_e_L',1000013:'Smu_L',1000014:'Snu_mu_L',1000015:'Stau_1',1000016:'Snu_tau_L',
	2000011:'Se_R',2000013:'Smu_R',2000015:'Stau_2',
    1000021:'Sg',
	1000022:'N1',1000023:'N2',1000024:'C1',1000025:'N3',1000035:'N4',1000037:'C2',1000045:'N5',
	}
block_code_name['MINPAR']={
    0:'scale',3:'tanB'
}
block_code_name['EXTPAR']={
    1:'M1',2:'M2',3:'M3',
    61:'Lambda',62:'Kappa',63:'Alambda',64:'Akappa',65:'Mu_eff',
    124:'MA',125:'MP'
}
block_code_name['ABUNDANCE']={
    0:'mDM',4:'DMRD'
}
block_code_name['NDMCROSSSECT']={
    1:'Psi',2:'Nsi',3:'Psd',4:'Nsd'
}

# block_code_name['EXTPAR']={
    
# }


class standard_form_data():
    def _AnalyseStandardLine(in_line):
        if in_line=='':
            return None
        else:
            line=in_line.strip()
            if len(line)==0:
                return '#'
            elif line[0]=='#':
                return '#'
            else:
                row=line.split('\t')
                col_name=['No.']
                value_row=[int(row[0])]
                for name_value in row[1:]:
                    nv_list=name_value.split(':')
                    # col_name.append(StringToIFT(nv_list[0]))
                    col_name.append(nv_list[0])
                    value_row.append(StringToIFT(nv_list[1]))
            return DataFrame(numpy.array([value_row]),columns=col_name)
                        
    def ReadStandardData(file_name):
        Data=DataFrame({})
        f=open(file_name,'r')
        while True:
            new_line=standard_form_data._AnalyseStandardLine(f.readline())
            if type(new_line) is DataFrame:
                Data=Data.append(new_line,ignore_index=True)
            elif new_line == '#':
                continue
            elif new_line==None:
                break
        f.close()
        return Data