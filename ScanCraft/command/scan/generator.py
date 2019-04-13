#! /usr/bin/env python3
import numpy
class generators():
    '''functions for .free_parameter'''
    def uniform(self):
        self.value = numpy.random.uniform(low=self.minimum,high=self.maximum)
    def exponential(self):
        # lambda=6.9314718055994529: Cumulative distribution=0.5 at x=0.1
        # scale=1/lambda
        while True:
            new_value=numpy.random.exponential(scale=0.144)
            if self.minimum<new_value<self.maximum:
                break
        self.value = new_value
    def normal(self,step_factor=1.):
        new_value=numpy.nan
        while not all([new_value>self.minimum, new_value<self.maximum]):
            new_value=numpy.random.normal(loc=self.value
                ,scale=self.step_width*step_factor
                )
        self.value=new_value
    def lognormal(self,step_factor=1.):
        new_value=numpy.nan
        while not all([new_value>self.minimum, new_value<self.maximum]):
            new_value=numpy.random.lognormal(mean=numpy.log(self.value)
                ,sigma=self.step_width*step_factor
            )
        self.value=new_value