#!/usr/bin/env python3
import numpy,copy,math
from .data_type import scalar,matrix
from .read.readline import ReadLine
from .color_print import *
from .read.readSLHA import ReadSLHAFile

class Random():
    def normal(mean,minimum,maximum,step_factor=1.):
        deviation=(maximum-minimum)/100.*step_factor
        v=numpy.random.normal(mean,deviation)
        return max( minimum, min( maximum, v ) )
    def lognormal(mean,minimum,maximum,step_factor=1.):
        log_mean=math.log(mean)
        log_deviation=math.log(maximum/minimum)/100.*step_factor
        v=numpy.random.lognormal(log_mean,log_deviation)
        return max( minimum, min( maximum, v ) )

class data_list():
    pass

class scan():
    def __init__(self,method='mcmc'):
        self.variable_list={}
        self.scalar_list={}
        self.matrix_list={}
        self.follow_list={}
        self.block_list={}

        if method.lower()=='mcmc':
            self.Add=self.AddMcmcScalar
            self.AddMatrix=self.AddMcmcMatrix
            self.GetNewPoint=self.GetNewPoint_mcmc
        elif method.lower()=='random':
            self.Add=self.AddMcmcScalar
            self.AddMatrix=self.AddMcmcMatrix
            self.GetNewPoint=



    def AddMcmcScalar(self,name,block,PDG,minimum=None,maximum=None,pace='normal',step_width=None,value=None):
        block=block.upper()

        # set one scalar
        scl=scalar(name,block,PDG,value)
        
        # set scan strategy
        pace=pace.split()
        if pace[0].lower() not in ('normal','lognormal','follow'):
            Caution("'pace' should be 'normal', 'lognormal' or 'follow name_of_target'")
            exit()
        scl.pace=pace[0].lower()
        if scl.pace=='follow':
            scl.follow=pace[1]
            self.follow_list[name]=scl
        else:
            scl.minimum=minimum
            scl.maximum=maximum

            if step_width:
                scl.step_width=step_width
            else:
                try:
                    scl.step_width=(scl.maximum-scl.minimum)/100.
                except TypeError:
                    Caution(
                        "  Both maximum and minimum of '%s' should be given with pace='%s'"%(name,pace[0])
                    +   " if step width is not specified. Later, step width will be 1% of its initial value")

            # add scalar into lists
            self.scalar_list[name]=scl

        if name in self.variable_list.keys():
            Caution("scalar '%s' overridden"%name)
        self.variable_list[name]=scl
        if block not in self.block_list.keys():
            self.block_list[block]={}
        block_i=self.block_list[block]
        block_i[PDG]=scl
    
    def AddMcmcMatrix(self,name,block,shape,free_element={},minimum=None,maximum=None,pace='normal',step_width=None,element_list={}):
        block=block.upper()
        # set one matrix
        mtx=matrix(name,block,shape,element_list={})
        
        if type(free_element) is dict:
            mtx.element_list.update(free_element)
        elif type(free_element) is list or type(free_element) is tuple:
            if all( type(coords) is tuple for coords in free_element ):
                mtx.element_list.update(dict.fromkeys(free_element))

        mtx.minimum=minimum
        mtx.maximum=maximum
        mtx.pace=pace
        if step_width:
            mtx.step_width=step_width
        else:
            try:
                mtx.step_width=(mtx.maximum-mtx.minimum)/100.
            except TypeError:
                Caution(
                    "  Both maximum and minimum of '%s' should be given with pace='%s'"%(name,pace[0])
                +   " if step width is not specified. Later, step width will be 1% of its initial value")

        # add matrix into lists
        if name in self.variable_list.keys():
            Caution("parameter '%s' overridden"%name)
        self.variable_list[name]=mtx
        self.matrix_list[name]=mtx

        if block in self.block_list.keys():
            Caution("matrix '%s' overridden"%name)
        self.block_list[block]=mtx

    def GetNewPoint_mcmc(self,step_factor=1.):
        new_point=copy.deepcopy(self)
        for name in self.scalar_list.keys():
            old=self.scalar_list[name]
            v=getattr(Random,old.pace)(old.value , old.minimum , old.maximum ,step_factor)
            new_point.scalar_list[name].value=v
        for name in self.follow_list.keys():
            par=new_point.follow_list[name]
            par.value=new_point.variable_list[par.follow].value
        for name in self.matrix_list.keys():
            old=self.matrix_list[name]
            for coords in old.element_list.keys():
                v=getattr(Random,old.pace)(old.element_list[coords] , old.minimum , old.maximum ,step_factor)
                new_point.matrix_list[name].element_list[coords]=v
        return new_point
    
    def Print(self):
        for name in self.scalar_list.keys():
            print('\t',name,self.scalar_list[name].value)
        for name in self.follow_list.keys():
            print('\t',name,self.follow_list[name].value)
        for name in self.matrix_list.keys():
            print('\t',name,self.matrix_list[name].element_list)
            

    def GetValue(self,file_name):
        target=data_list()
        ReadSLHAFile(file_name,target)
        #print(target.LAMN);exit()
        for name in self.scalar_list.keys():
            par=self.scalar_list[name]
            par.value=getattr(target,par.block)[par.PDG]
        for name in self.follow_list.keys():
            par=self.follow_list[name]
            par.value=self.variable_list[par.follow].value
        for name in self.matrix_list.keys():
            par=self.matrix_list[name]
            for coords in par.element_list.keys():
                par.element_list[coords]=getattr(target,par.block[:])[coords]