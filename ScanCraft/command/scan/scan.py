#!/usr/bin/env python3
import numpy,copy,math
# from .data_type import scalar,matrix
from collections import ChainMap
from ..read.readline import ReadLine
from ..color_print import Error,Caution
from ..DataProcessing.SLHA.SLHA_picklable import SLHA_document
from .free_parameter import independent_scalar,independent_element,follower,dependent_scalar
from ..format.parameter_type import scalar

default_pdf={
    'random':'uniform',
    'mcmc'  :'normal'
    }


class scan():
    def __init__(self,method='mcmc'):

        self.scalar_list={}
        self.element_list={}
        self.follower_list={}
        self.dependent_list={}
        # self.matrix_list={}
        # self.free_parameter_list={}

        self.variable_dict=ChainMap(
            self.scalar_list,self.element_list,self.follower_list,self.dependent_list
        )
        self.free_parameter_list=ChainMap(
            self.scalar_list,self.element_list
        )

        self.block_list={}

        self.method=method.lower()

        # if self.method=='mcmc':
        #     self.Add=self.AddMcmcScalar
        #     self.AddMatrix=self.AddMcmcMatrix
        #     self.GetNewPoint=self.GetNewPoint_mcmc

    def AddToList(self,par):
        if par.name in self.variable_dict.keys():# check duplicates
            Caution("parameter '%s' will be overridden"%name)
            goon=input('contineu? (y/n[n])')
            if not goon in ['y','Y']:
                exit()

        # self.variable_list.update({par.name:par})
        # No longer need after variable_list became ChainMap type

        if type(par) is independent_scalar:
            self.scalar_list.update({par.name:par})
        elif type(par) is independent_element:
            self.element_list.update({par.name:par})
        elif type(par) is follower:
            self.follower_list.update({par.name:par})
        elif type(par) is dependent_scalar:
            self.dependent_list.update({par.name:par})

        if par.block not in self.block_list.keys():
            self.block_list.update({par.block:{}})
        block_i=self.block_list[par.block]
        block_i.update({par.code:par})

    def AddScalar(self,name,block,code
            ,minimum=None,maximum=None,value=None
            ,prior_distribution=None
            ,step_width=None
            ,**args
        ):
        if prior_distribution==None:
            prior_distribution={#defult prior
            'random':'uniform','mcmc':'normal'
            }[self.method]

        scl=independent_scalar(
            name,block,code,minimum,maximum,value=value
            ,strategy=self.method
            ,prior_distribution=prior_distribution
            ,**args)
        self.AddToList(scl)

    def AddElement(self,name,block,code
            ,minimum=None,maximum=None,value=None
            ,prior_distribution=None
            ,step_width=None
            ,**args
        ):
        if prior_distribution==None:
            prior_distribution={#defult prior
            'random':'uniform','mcmc':'normal'
            }[self.method]

        elm=independent_element(
            name,block,code,minimum,maximum
            ,strategy=self.method
            ,prior_distribution=prior_distribution
            ,**args)
        self.AddToList(elm)

    def AddDependent(self,name,block,code,func=None,variables=None,value=None):
        variable_list=[]
        try:# replace parameter names in variables with parameter objects,
            # then collect them into variable_list
            for var in variables:
                if type(var) is str:
                    var=self.variable_dict[var]
                variable_list.append(var)
        except KeyError:
            Error('variable %s do not exist'%var)
        except TypeError:
            pass
        dpd=dependent_scalar(name,block,code,func,variable_list,value)
        self.AddToList(dpd)

    def AddFollower(self,name,block,code,target):
        if type(target) is str:
            try:
                target=self.variable_dict[target]
            except KeyError:
                Error('variable %s do not exist'%target)
        while isinstance(target,(follower)):
            target=target.target
        flw=follower(name,block,code,target)
        self.AddToList(flw)
    

    def AddMatrix(self,name,block):
        pass

    def Sample(self,**keys):
        for p in self.free_parameter_list.values():
            p.Generate(**keys)
        return copy.deepcopy(self)
    #========================
    
    def Print(self):
        for name,par in sorted(self.variable_dict.items()):
            print(f'{name:>10}: {par.value}')
        #   print('\t',name,self.scalar_list[name].value)
        # for name in self.follower_list.keys():
        #     print('\t',name,self.follower_list[name].value)
        # for name in self.matrix_list.keys():
        #     print('\t',name,self.matrix_list[name].element_list)
            

    def GetValue(self,file_name,mapping:dict={},ignore:list=[],read_func=None):
        '''Arguments
      Required:
          file_name: SLHA file that contain needed parameters;
      Optional:
           mapping : A dict which holds a map of different block names: 
                     { name in object : name in SLHA file }
            ignore : parameters with name in this will not be read
            read_func   : The function that will analyse the SLHA file
        '''
        if read_func is None:
            read_func=SLHA_document
        target=read_func(file_name)
        # print(mapping)
        for par in self.free_parameter_list.values():
            if par.name in ignore:continue
            par.value=target(par.block,par.code)