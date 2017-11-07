import numpy
import sys
import os

sys.path.append("%s/liangbin/"%os.environ["HOME"])
import lexcel_head

def read(title_file, data_file, skip=[], mode=1):
  """
1: for easyscan format
"""
  if mode==1:
    lines=open(title_file, "r").readlines()
    #print lines
    title=["+".join(line.split()[:-1]) for line in lines[1:]]
    #print title
    text=open(data_file, "r").read()
    with open("tmp_%s"%data_file,"w") as f:
       for i in title:
         f.write(i+"  ")
       f.write("\n%s"%text)
    for item in skip:
      lexcel_head.del_row("tmp_%s"%data_file, item)
    data=numpy.genfromtxt("tmp_%s"%data_file, delimiter=None, names=True, dtype=None)

  return data

