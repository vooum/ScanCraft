#!/usr/bin/env python3

class SLHA_string(str):
    def __init__(self,string):
        string=string.strip(' \t\n')
        self.commented_out=string.startswith('#') # True if this sentence is commented out
        string=string.lstrip(' \t#')
        self.blank = not bool(string) # whether a blank line
        if self.blank:
            return
        
        splited=string.split('#',maxsplit=1)
        self.string=splited[0]
        try:
            self.annotation=splited[1] # store annatation here
        except IndexError:
            self.annotation=''
            
#         self.semanteme=tuple([InterpretStr(i) for i in self.string.split()])
#     def __getitem__(self,key):
#         return self.semanteme[key]