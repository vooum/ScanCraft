#!/usr/bin/env python3

import torch
# from torch.autograd import Variable
from torch import nn
from torch.nn import functional as F

class Estimate(nn.Module):
    def __init__(self,D_in,d1,d2):
        super(Estimate,self).__init__()
        self.l1=torch.nn.Linear(D_in, d1)
        self.l2=torch.nn.Linear(d1,d2)
        self.l3=torch.nn.Linear(d2,3)
    def forward(self,x):
        x=self.l1(x)
        x=self.l2(x)
        x=F.leaky_relu(x)
        x=self.l3(x)
        return x

MSELoss=nn.MSELoss()
