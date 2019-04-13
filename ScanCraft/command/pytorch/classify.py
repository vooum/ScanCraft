#!/usr/bin/env python3

import torch
# from torch.autograd import Variable
from torch import nn
from torch.nn.init import uniform as U

class Classify(nn.Module):
    def __init__(self,D_in,d1,d2):
        super(Classify,self).__init__()
        self.l1=torch.nn.Linear(D_in, d1).double()
        self.l2=torch.nn.Linear(d1,d2).double()
        self.l3=torch.nn.Linear(d2,1).double()
        self.init()
    def init(self):
        U(self.l1.weight,a=-0.5,b=0.5)
        U(self.l2.weight,a=-0.5,b=0.5)
        U(self.l3.weight,a=-0.5,b=0.5)
    def forward(self,x):
        x=self.l1(x)
        x=nn.functional.dropout(x,p=0.5)
        x=nn.functional.leaky_relu(x)
        x=self.l2(x)
        x=nn.functional.dropout(x,p=0.5)
        x=nn.functional.leaky_relu(x)
        x=self.l3(x)
        #x=functional.sigmoid(x)
        return x

#BCEloss=nn.BCELoss(size_average=False)
BCEloss=nn.BCEWithLogitsLoss(size_average=False)