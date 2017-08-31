#!/usr/bin/env python3
import random,math
class generate:
    def randomflat(variable):
        return random.uniform(variable.min,variable.max) 
    def randomlog(variable):
        logmax=math.log10(variable.max)
        logmin=math.log10(variable.min)
        logvalue=random.uniform(logmin,logmax)
        return 10**logvalue