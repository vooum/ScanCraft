#!/usr/bin/env python3

import torch
from torch.autograd import Variable
from torch import nn

class Classify(nn.Module):
    def __init__(self,D_in,d1,d2):
        super(model,self).__init__()
        self.l1=torch.nn.Linear(D_in, d1)
        self.l2=torch.nn.Linear(d1,d2)
        self.l3=torch.nn.Linear(d2,1)
    def forward(self,x):
        x=self.l1(x)
        x=nn.functional.relu(x)
        x=torch.sqrt(x)
        x=self.l2(x)
        x=nn.functional.leaky_relu(x)
        x=self.l3(x)
        x=torch.nn.functional.sigmoid(x)
        return x

