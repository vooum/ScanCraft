#!/usr/bin/env python3

def GetBlockName(line):
    return line.split()[1].upper()

def GetDecayCode(line):
    return int(line.split()[1])

def commented_out(line):
    try:
        commented=(line.lstrip()[0]=='#')
    except IndexError:
        return True
    else:
        return commented

def interpret_str(string):
    try:
        out=float(string)
        return out
    except ValueError:
        try:
            out=float(string.upper().replace('D','E',1))
        except ValueError:
            out=string
    return out

def ReadLine(line):
    stripped=line.lstrip(' #\t').rstrip(' \t\n').split('#',maxsplit=1)
    #if not stripped[0]: return None #--------------> empty line
    semanteme=[interpret_str(i) for i in stripped[0].split()]
    try:
        note='#'+stripped[1]
    except IndexError:
        pass
    else:
        semanteme.extend([note])
    finally:
        return semanteme #-------------------------> [ infos, annotation, whether commented out ]
