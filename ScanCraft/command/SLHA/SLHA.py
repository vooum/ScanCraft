#!/usr/bin/env python3

flat_to_str=lambda L: sum(map(flat_to_str,L),[]) if isinstance(L,(list,tuple)) else [str(L)]

class list_block():
    def __init__(self,PDG_name_dict):
        self.PDG_name_dict=PDG_name_dict
    def __call__(self,number):
        return self.PDG_name_dict[number]
            
class matrix_block():
    def __init__(self,name):
        self.name=name
    def __call__(self,element):
        return '_'.join(flat_to_str([self.name,element]))
        

class SLHA():
    MNPAR=list_block({3:'tanB'})
    HMIX=matrix_block('Hmix')

# try: SLHA.HMIX((3,3))
#      SLHA.MNPAR(3)