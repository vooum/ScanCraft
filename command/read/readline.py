#!/usr/bin/env python3

def interpret_str(string):
    try:
        out=int(string)
    except ValueError:
        try:
            out=float(string)
            return out
        except ValueError:
            try:
                out=float(string.upper().replace('D','E',1))
            except ValueError:
                out=string
    return out


def readline(line):
    # semanteme：list of PDG codes, values, or matrix coordinates .etc
    try:
        comment_out=(line.lstrip()[0]=='#')
    except IndexError:
        return None #----------------------------------> empty line
    else:
        stripped=line.strip(' #\t\n').split('#',maxsplit=1)
        #if not stripped[0]: return None #--------------> empty line
        semanteme=[interpret_str(i) for i in stripped[0].split()]
        try:
            note='#'+stripped[1]
        except IndexError:
            note=''
        finally:
            semanteme.extend([note,comment_out])
            return semanteme #-------------------------> [ infos, annotation, whether commented out ]

if __name__=='__main__':
    #string='\t 1 1..5e3 1d5 aa# 1#a # \t\n'
    string='##\n'
    print(readline(string))