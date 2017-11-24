#!/usr/bin/env python3

from ..format.parameter_type import scalar,matrix
from .generator import generators
from ..color_print import Error

class independent_scalar(scalar,generators):
    def __init__(self,name,block,code
                ,minimum=None,maximum=None,value=None
                ,strategy='random'
                ,prior_distribution='uniform'
                ,**args
                ):
        super().__init__(name,block,code,value)
        self.minimum=minimum
        self.maximum=maximum
        self.value=value
        self.strategy=strategy
        self.prior_distribution=prior_distribution

        self.check(**args)
        self.Generate=getattr(self,prior_distribution)

    # def check(self,**args):
    #     if self.strategy=='random':
    #         if any([ getattr(self,i) is None for i in ('minimum','maximum')]):
    #             Error('unknown bounds of parameter %s '%self.name)
    #     else:
    #         Error('Unknown strategy: %s'%self.strategy)

class follower(scalar):
    def __init__(self,name,block,code,target):
        super().__init__(name,block,code)
        self.target=target
    def Generate(self):
        self.value=self.target.value