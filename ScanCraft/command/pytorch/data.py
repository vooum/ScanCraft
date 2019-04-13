#!/usr/bin/env python3

import torch
import pandas,numpy
from torch.cuda import DoubleTensor as Tensor
from command.pytorch.normalize import normalize


class data():
    def ReadData(self,filelist):
        # self.filelist=filelist

        self.acc_list=[pandas.read_csv(filelist['accepted'][i],header=[0,1,2,3],index_col=0) 
         for i in sorted( list(filelist['accepted'].keys()), reverse=True) ]
        self.exc_list=[pandas.read_csv(filelist['excluded'][i],header=[0,1,2,3],index_col=0) 
         for i in sorted( list(filelist['excluded'].keys()), reverse=True) ]
        self.mass_list=[pandas.read_csv(filelist['mass'][i],header=[0,1],index_col=0) 
         for i in sorted( list(filelist['mass'].keys()), reverse=True ) ]
        
        self.acc=pandas.concat(self.acc_list,ignore_index=True)
        self.exc=pandas.concat(self.exc_list,ignore_index=True)
        self.mass =pandas.concat(self.mass_list, ignore_index=True)
    def SetNorm(self,mold):
        self.Norm=normalize(mold)
    def Add(self,acc_new,exc_new,mass_new):
        self.acc_list.insert(0,acc_new)
        self.exc_list.insert(0,exc_new)
        self.mass_list.insert(0,mass_new)

        self.acc=panndas.concat([acc_new,self.acc],ignore_index=True)
        self.exc=panndas.concat([exc_new,self.exc],ignore_index=True)
        self.mass=panndas.concat([mass_new,self.mass],ignore_index=True)
    def GetTensor(self,start=None,end=50000):
        self.c_data=numpy.vstack((self.acc.values[start:end],self.exc.values[start:end]))
        self.c_in=Tensor(
            self.Norm(self.c_data[:,:7])
            )
        self.c_target=Tensor(
            self.c_data[:,-1].reshape( (len(self.c_data),1) )
            )
        
        self.e_data=numpy.hstack(
            (self.acc.values,numpy.log10(self.mass.values))
            )[start:end]
        self.e_in=Tensor(self.Norm(self.e_data[:,:7]))
        self.e_target=Tensor(self.e_data[:,-3:])
        return [self.c_in,self.c_target,self.e_in,self.e_target]