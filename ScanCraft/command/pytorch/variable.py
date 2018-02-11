#!/usr/bin/env python3

from torch import FloatTensor
from torch.autograd import Variable

# def CudaVariableFromArray(array,**keys):
#     return Variable(FloatTensor(array).cuda(),**keys)

def ArrayFromCudaVariable(var):
    return var.cpu().data.numpy()