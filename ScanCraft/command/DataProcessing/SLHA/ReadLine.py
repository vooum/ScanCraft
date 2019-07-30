#!/usr/bin/env python3

def GetBlockName(line):
    return line.split()[1].upper()

def GetDecayCode(line):
    return int(line.split()[1])