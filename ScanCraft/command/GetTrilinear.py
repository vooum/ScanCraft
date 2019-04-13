#!/usr/bin/env python3

'''
Function: perform some preliminart calculation
Notes:
   alamn_11=0
   alamn_22=0
   Av_11=0

Functionalized by He Yangle @ 2018.07.24
''' 

import math

def GetTrilinear(*data):
# data: Yv_33 LAMN_33 alamn_33 Av_11 Av_33 Au_33 mu Lambda tanbeta
    mt=173.5
    mb=4.18
    Yv_33=data[0]
    Yv_22=Yv_33
    Yv_11=Yv_33

    LAMN_33=data[1]
    LAMN_22=3.6*LAMN_33
    LAMN_11=4.0*LAMN_33

    alamn_33=data[2]
    alamn_11=alamn_33
    alamn_22=alamn_33

    Av_11=data[3]
    Av_22=Av_11
    Av_33=data[4]


    Au_33=data[5]
    Ad_33=Au_33

    mu=data[6]
    Lambda=data[7]
    tanbeta=data[8]
    v=246.0
    Yu_33=mt/(v*math.sin(math.atan(tanbeta)))
    Yd_33=mb/(v*math.cos(math.atan(tanbeta)))

    Tv_11=Yv_11*Av_11
    Tv_22=Yv_22*Av_22
    Tv_33=Yv_33*Av_33
    tlamn_11=LAMN_11*alamn_11
    tlamn_22=LAMN_22*alamn_22
    tlamn_33=LAMN_33*alamn_33
    TU_33=Au_33*Yu_33
    TD_33=Ad_33*Yd_33
    vs=sqrt(2.0)*mu/Lambda

    return (Tv_11, Tv_22, Tv_33, tlamn_11, tlamn_22, tlamn_33,TU_33,TD_33,vs)