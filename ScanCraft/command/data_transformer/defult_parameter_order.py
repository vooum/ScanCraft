#!/usr/bin/env python3

import copy
from ..scan.free_parameter import independent_scalar, independent_element
input_parameter_list=[
    'tanB',
    'M1',
    'M2',
    'M3',
    'Atop',
    'Atau',
    'MQ3L',
    'MtopR',
    'Lambda',
    'Kappa',
    'A_Lambda',
    'A_kappa',
    'mu_eff',
    ]

def defult_name_order(par_dict):
    disorder_scalars =[ name for name in par_dict.keys() if type(par_dict[name]) is independent_scalar ]
    disorder_elements=[ name for name in par_dict.keys() if type(par_dict[name]) is independent_element]
    ordered=[]
    for name in input_parameter_list:#scalars
        if name in disorder_scalars:
            ordered.append(name)
            disorder_scalars.remove(name)
    if len(disorder_scalars)>0:
        print(disorder_scalars)
        exit('Unknown scalar names, add them into input_parameter_list')

    matrixes=set([i.split('_')[0] for i in disorder_elements])
    for name in input_parameter_list:#matrix elements
        if name in matrixes:
            elements = sorted([n_e for n_e in disorder_elements if name in n_e])
            ordered.extend(elements)
            elements.clear()
            for n_e in elements:
                disorder_elements.remove(n_e)
    if len(disorder_elements)>0:
        print(disorder_elements)
        exit('Unknown element names, add them into input_parameter_list')
    
    return ordered