#!/usr/bin/env python3

flat_to_str=lambda L: sum(map(flat_to_str,L),[]) if isinstance(L,(list,tuple)) else [str(L)] #sum([[3],[3]],[])可得[3,3]

class list_block():
    def __init__(self,PDG_name_dict):
        self.PDG_name_dict=PDG_name_dict
    def __call__(self,number):
        return self.PDG_name_dict[number]
            
class matrix_block():
    def __init__(self,name):
        self.name=name
    def __call__(self,element):
        return '_'.join(flat_to_str([self.name,element]))  #例如self.name=Hmix,element=(3,3) 它们组成列表[Hmix,3,3],

SMINPUTS={1:'ALPHA_EM^-1(MZ)',2:'GF',3:'ALPHA_S(MZ)',
          4:'MZ',5:'MB',6:'MTOP',7:'MTAU'}        
MINPAR={3:'tanB',0:'SCALE'}
EXTPAR={1:'M1',2:'M2',3:'M3',
        11:'Atop',12:'Abottom',
        13:'Atau',16:'Amuon',
        31:'L1',32:'L2',33:'L3',
        34:'E1',35:'E2',36:'E3',
        41:'Q1',42:'Q2',43:'Q3',
        44:'U1',45:'U2',46:'U3',
        47:'D1',48:'D2',49:'D3',
        61:'Lambda',62:'Kappa',63:'ALambda',64:'AKappa',
        65:'MUEFF',124:'MA_QSTSB'}
MASS={5:'MB',6:'MTOP',15:'MTAU',23:'MZ',24:'MW',
      25:'H1',35:'H2',45:'H3',36:'A1',46:'A2',37:'C1',
      1000001:'~d_L',2000001:'~d_R',1000002:'~u_L',2000002:'~u_R',
      1000003:'~s_L',2000003:'~s_R',1000004:'~c_L',2000004:'~c_R',
      1000005:'~b_1',2000005:'~b_2',1000006:'~t_1',2000006:'~t_2',
      1000011:'~e_L',2000011:'~e_R',1000012:'snu_1',
      1000013:'~mu_L',2000013:'~mu_R',1000014:'snu_2',
      1000015:'~tau_L',2000015:'~tau_R',1000016:'snu_3',1000021:'~g',
      1000022:'N1',1000023:'N2',1000025:'N3',1000035:'N4',1000045:'N5',
      1000024:'ch1',1000037:'ch2',1000039:'gravitino'}
LOWEN={1:'BR(b->s_gamma)',11:'BR(b->s_gamma+Theor_Err)',12:'BR(b->s_gamma-Theor_Err)',
       2:'DeltaM_d_ps^-1',21:'DeltaM_d+Theor_Err',22:'DeltaM_d-Theor_Err',
       3:'DetaM_s',31:'DeltaM_s+Theor_Err',32:'DeltaM_s-Theor_Err',
       4:'BR(Bs->mu+mu-)',41:'BR(Bs->mu+mu-)+Theor_Err',42:'BR(Bs->mu+mu-)-Theor_Err',
       5:'BR(B+->tau+nu_tau)',51:'BR(B+->tau+nu_tau)+Theor_Err',52:'BR(B+->tau+nu_tau)-Theor_Err',
       6:'Del_a_mu',61:'Del_a_mu+Theor_Err',62:'Del_a_mu-Theor_Err'}
HMIX={1:'MUEFF',2:'tanB',3:'VQ',4:'MA^2',5:'MP^2'}
GAUGE={1:'g1',2:'g2',3:'g3'}
MSOFT={1:'M1',2:'M2',3:'M3',21:'M_HD',22:'M_HU',31:'M_eL',32:'M_muL',33:'M_tauL',
       34:'M_eR',35:'M_muR',36:'M_tauR',41:'M_q1L',42:'M_q2L',43:'M_q3L',
       44:'M_uR',45:'M_cR',46:'M_tR',47:'M_dR',48:'M_sR',49:'M_bR'}
NMSSMRUN={1:'Lambda',2:'Kappa',3:'ALambda',4:'AKappa',5:'MUEFF',
          6:'XIF',7:'XIS',8:'MUP',9:'MSP',10:'MS'}
GUTGAUGE={1:'GUTg1',2:'GUTg2',3:'GUTg3'}
GUTMSOFT={1:'GUT_M1',2:'GUT_M2',3:'GUT_M3',21:'GUTM_HD',22:'GUTM_HU',31:'GUTM_eL',32:'GUTM_muL',33:'GUTM_tauL',
          34:'GUTM_eR',35:'GUTM_muR',36:'GUTM_tauR',41:'GUTM_q1L',42:'GUTM_q2L',43:'GUTM_q3L',
          44:'GUTM_uR',45:'GUTM_cR',46:'GUTM_tR',47:'GUTM_dR',48:'GUTM_sR',49:'GUTM_bR'}
GUTNMSSMRUN={1:'GUT_Lambda',2:'GUT_Kappa',3:'GUT_ALambda',4:'GUT_AKappa',5:'GUT_MUEFF',
             6:'GUT_XIF',7:'GUT_XIS',8:'GUT_MUP',9:'GUT_MSP',10:'GUT_MS',12:'GUT_M3H'}
FINETUNING={1:'PS=MHU',2:'PS=MHD',3:'PS=MS',4:'PS=ALambda',5:'PS=AKappa',
            6:'PS=XIF',7:'PS=XIS',8:'PS=MUP',9:'PS=MSP',10:'PS=M3H',
            11:'PS=LAMBDA',12:'PS=KAPPA',13:'PS=HTOP',14:'PS=G',15:'MAX',16:'IMAX'}
LHCCROSSSECTIONS={11:'VBF/VH->H1->tautau',
                  13:'VBF/VH->H1->bb',
                  15:'VBF/VH->H1->ZZ/WW',
                  17:'VBF/VH->H1->gammagamma',
                  19:'VBF/VH->H1->invisible',
                  21:'VBF/VH->H2->tautau',
                  23:'VBF/VH->H2->bb',
                  25:'VBF/VH->H2->ZZ/WW',
                  27:'VBF/VH->H2->gammagamma',
                  29:'VBF/VH->H2->invisible',
                  31:'VBF/VH->H3->tautau',
                  33:'VBF/VH->H3->bb',
                  35:'VBF/VH->H3->ZZ/WW',
                  37:'VBF/VH->H3->gammagamma',
                  39:'VBF/VH->H3->invisible',
                  12:'ggf->H1->tautau',
                  14:'ggf->H1->bb',
                  16:'ggf->H1->ZZ/WW',
                  18:'ggf->H1->gammagamma',
                  110:'ggf->H1->invisible',
                  22:'ggf->H2->tautau',
                  24:'ggf->H2->bb',
                  26:'ggf->H2->ZZ/WW',
                  28:'ggf->H2->gammagamma',
                  210:'ggf->H2->invisible',
                  32:'ggf->H3->tautau',
                  34:'ggf->H3->bb',
                  36:'ggf->H3->ZZ/WW',
                  38:'ggf->H3->gammagamma',
                  310:'ggf->H3->invisible',}
LHCFIT={1:'Hgammagamma',2:'Hff',3:'HVV'}


class SLHA():
    SMINPUTS=list_block(SMINPUTS)
    MINPAR=list_block(MINPAR)
    EXTPAR=list_block(EXTPAR)
    MASS=list_block(MASS)
    LOWEN=list_block(LOWEN)
    HMIX=list_block(HMIX)
    GAUGE=list_block(GAUGE)
    NMSSMRUN=list_block(NMSSMRUN)
    GUTGAUGE=list_block(GUTGAUGE)
    GUTMSOFT=list_block(GUTMSOFT)
    GUTNMSSMRUN=list_block(GUTNMSSMRUN)
    FINETUNING=list_block(FINETUNING)
    LHCCROSSSECTIONS=list_block(LHCCROSSSECTIONS)
    LHCFIT=list_block(LHCFIT)
    NMHMIX=matrix_block('NMHMIX')
    NMAMIX=matrix_block('NMAMIX')
    STOPMIX=matrix_block('STOPMIX')
    SBOTMIX=matrix_block('SBOTMIX')
    STAUMIX=matrix_block('STAUMIX')
    NMNMIX=matrix_block('NMNMIX')
    UMIX=matrix_block('UMIX')
    VMIX=matrix_block('VMIX')
    REDCOUP=matrix_block('REDCOUP')
    YU=matrix_block('YU')
    YD=matrix_block('YD')
    YE=matrix_block('YE')
    AU=matrix_block('AU')
    TU=matrix_block('TU')
    AD=matrix_block('AD')
    TD=matrix_block('TD')
    AE=matrix_block('AE')
    TE=matrix_block('TE')
    MSQ2=matrix_block('MSQ2')
    MSU2=matrix_block('MSU2')
    MSD2=matrix_block('MSD2')
    MSL2=matrix_block('MSL2')
    MSE2=matrix_block('MSE2')
    USQMIX=matrix_block('USQMIX')
    DSQMIX=matrix_block('DSQMIX')
    SELMIX=matrix_block('SELMIX')
    GUTYU=matrix_block('GUTYU')
    GUTYD=matrix_block('GUTYD')
    GUTYE=matrix_block('GUTYE')
    GUTAU=matrix_block('GUTAU')
    GUTAD=matrix_block('GUTAD')
    GUTAE=matrix_block('GUTAE')
    


