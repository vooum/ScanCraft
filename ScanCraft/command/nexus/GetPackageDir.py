#! /usr/bin/env python3
import os
try:
    from ..color_print import Error
except:
    pass
def GetPackageDir(name,silent=False):
    candidate=[]
    package_path=os.path.join(
        os.path.dirname(# Scancommando/
            os.path.dirname(# .command/
                os.path.dirname(__file__)))# .command/operations/
                ,'packages/')
    for i in os.listdir(package_path):
        if name in i:
            package=os.path.join(package_path,i)
            if os.path.isdir(package):
                if not silent:
                    print('%s file:\n->%s'%(name,package))
                candidate.append(package)
    if len(candidate)==0:
        Error('%s package not found in %s'%(name,package_path))
    elif len(candidate)==1:
        return candidate[0]+'/'
    else:
        package_list='\n\t'.join(candidate)
        Error('Found more than one packages including \'%s\':\n\t%s\n  more details needed.'%(name,package_list))