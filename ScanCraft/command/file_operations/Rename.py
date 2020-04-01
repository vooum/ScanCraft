#! /usr/bin/env python3
import time,os,shutil

def Tag_ctime(old_dir):
    ctime=time.strftime("%Y%m%d_%H%M%S", time.localtime(os.path.getctime(old_dir)))
    new=old_dir+'_'+ctime
    shutil.move(old_dir,new)
    return new