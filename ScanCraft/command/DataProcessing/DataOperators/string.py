#!/usr/bin/env python3

def Dfloat(string):
    try:
        return float(string)
    except ValueError:
        return float(string.upper().replace('D','E',1))