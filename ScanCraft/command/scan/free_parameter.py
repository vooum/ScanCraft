#!/usr/bin/env python3

# import sys
import numpy
from ..format.parameter_type import scalar,matrix
from .generator import generators
from ..color_print import Error
# from ..operators.iterable import FlatToList

class independent_scalar(scalar,generators):
    def __init__(self,name,block,code
                ,minimum=None,maximum=None,value=None
                ,strategy='random'
                ,prior_distribution='uniform'
                ,step_width=None
                ,**args
                ):
        super().__init__(name,block,code,value)
        self.minimum=minimum
        self.maximum=maximum
        self.value=value
        self.strategy=strategy
        self.prior_distribution=prior_distribution
        self.step_width=step_width

        self.check(**args)
        self.Generate=getattr(self,prior_distribution)

    def check(self,**args):
        if self.strategy=='random':
            if any([ getattr(self,i) is None for i in ('minimum','maximum')]):
                Error('unknown bounds of parameter %s '%self.name)
        elif self.strategy=='mcmc':
            if not self.step_width:
                if any([ getattr(self,i) is None for i in ('minimum','maximum')]):
                    Error('unknown bounds of parameter %s '%self.name)
                else:
                    if self.prior_distribution=='normal':
                        self.step_width=(self.maximum-self.minimum)/100.
                    elif self.prior_distribution=='lognormal':
                        self.step_width=(numpy.log(self.maximum)-numpy.log(self.minimum))/100.
        else:
            Error('Unknown strategy: %s'%self.strategy)


class independent_element(independent_scalar):
    pass

class dependent_scalar(scalar):
    def __init__(self,name,block,code,
                func=None,variables=None,value=None):
        super().__init__(name,block,code,value)
        self.variables=variables
        self._value=value
        self.func=func
        if type(func) is str:
            if func=='follow':
                if len(self.variables)>1:
                    Error('more than one variables when func is follow')
                self.func=lambda x: x
    @property # redefine value
    def value(self):
        if self._value:
            return self._value
        else:
            if not any([self.func,self.variables]):
                Error(f'Please offer any of func/variable/value of {name}')
            return self.func(*[v.value for v in self.variables])
    @value.setter # prevent value attribute from assigning any values
    def value(self,value):
        self._value=value
    @value.deleter
    def value(self):
        self._value=None
    def __call__(self):
        return self.value


class follower(dependent_scalar):
    def __init__(self,name,block,code,target):
        super().__init__(name,block,code,
                        func='follow',variables=[target])
        self.target=target
    
class independent_matrix(matrix,generators):
    def __init__(self, name, block, shape = None, value = None, free_element_list=None):
        super().__init__(name, block, shape, value)
        self.free_elements={}
        self.follower_elements={}