#! /usr/bin/env python3

try:
    from ..data_type import data_list
    from .readline import commented_out,ReadLine
except:
    if __name__=='__main__':
        pass
    else:
        raise

def ReadDecay(text):
    semanteme=ReadLine(text.lines[text.i])
    if semanteme[0].upper()!='Decay':
        exit('wrong when entering ReadDecay')
    
    while True:
        try:
            line=text.NextLine()# iterator
        except IndexError:
            break

        semanteme=ReadLine(line)
        
