#!/usr/bin/env python3

import copy
from collections import namedtuple
from ..scan.free_parameter import independent_scalar, independent_element
# abandon
# input_parameter_list=[
#     'tanB',
#     'M1',
#     'M2',
#     'M3',
#     'Atop',
#     'Atau',
#     'MQ3L',
#     'MtopR',
#     'Lambda',
#     'Kappa',
#     'A_Lambda',
#     'A_kappa',
#     'mu_eff',
#     ]

# def defult_name_order_old(par_dict):
#     '''
#     return a list of names. All names of the parameters in par_dict are stored in this list.
#     First scalar names, then matrix name and elements' number, e.g. Yu_3_3.
#     '''
#     disorder_scalars =[ name for name in par_dict.keys() if type(par_dict[name]) is independent_scalar ]
#     disorder_elements=[ name for name in par_dict.keys() if type(par_dict[name]) is independent_element]
#     ordered=[]
#     for name in input_parameter_list:#scalars
#         if name in disorder_scalars:
#             ordered.append(name)
#             disorder_scalars.remove(name)
#     if len(disorder_scalars)>0:
#         print(disorder_scalars)
#         exit('Unknown scalar names, add them into input_parameter_list')

#     matrixes=set([i.split('_')[0] for i in disorder_elements])
#     for name in input_parameter_list:#matrix elements
#         if name in matrixes:
#             elements = sorted([n_e for n_e in disorder_elements if name in n_e])
#             ordered.extend(elements)
#             elements.clear()
#             for n_e in elements:
#                 disorder_elements.remove(n_e)
#     if len(disorder_elements)>0:
#         print(disorder_elements)
#         exit('Unknown element names, add them into input_parameter_list')
    
#     return ordered


block_list=['MINPAR','EXTPAR','MSOFT','MSQ2','MSU2','MSD2','MSL2','TU','TD','TE']

ID=namedtuple('identity_tuple',['block','code','name'])
class ID(namedtuple('identity_tuple',['block','code','name'])):
    __slots__=()
    def __str__(self):
        return f'{self.name:>10}:{self.block:>10}: {self.code}'
    def __lt__(self,other):
        b1=self.block
        b2=other.block
        try:
            b1=str(block_list.index(b1))
        except ValueError:
            pass
        try:
            b2=str(block_list.index(b2))
        except ValueError:
            pass
        if b1!=b2:
            # print(b1,b2,self.name,other.name)
            return b1<b2
        else:
            # print(self.code,other.code,self.name,other.name)
            return self.code<other.code

def defult_name_order(par_dict):
    ID_list=[ID(par.block,par.code,par.name)for par in par_dict.values()]
    # print(ID_list)
    return [i.name for i in sorted(ID_list)]
