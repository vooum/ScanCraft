#!/usr/bin/env python3
import shutil
from ..color_print import Error
def MergeAttributes(*objects):
    new_obj=capsule()
    for obj in objects:
        for key,value in obj.__dict__.items():
            setattr(new_obj,key,value)
    return new_obj


class capsule():
    '''container to store data in it,
    thus data can be accessed by .__dict__
    '''
    def Merge(self,*others):
        self.__dict__= MergeAttributes(self,*others).__dict__
    def MoveTo(self,destinations):
        keys=destinations.keys()
        if self.documents.keys()!=keys:
            Error('keys do not match while moving files')
        else:
            for key in keys:
                shutil.move(self.documents[key],destinations[key])
            self.documents.update(destinations)
    def CopyTo(self,destinations):
        keys=destinations.keys()
        for key in keys:
            try:
                shutil.copy(self.documents[key],destinations[key])
            except TypeError:
                if self.documents[key] is None:
                    destinations[key]=None
                else:
                    raise                
        self.documents.update(destinations)
    def EqualTo(self,other,block_list=None):
        if block_list is None:
            block_list=list(self.__dict__.keys())
            #print(block_list)
        eq=all([
            getattr(self,block)==getattr(other,block,list())
            for block in block_list
        ])
        return eq
    def __eq__(self,other):
        return self.EqualTo(other)
