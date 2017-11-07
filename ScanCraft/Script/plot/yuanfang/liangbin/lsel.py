import os
import sys
import glob

sys.path.append("%s/liangbin"%os.environ["HOME"])
import lslha

def sel(cut, val, eps, filename, foldername, mode="SLHA"):
  if len(cut)!=3:
    print("Error: wrong argu \"cut\" in function lsel.sel!")
    sys.exit()

  outfolder="tmp_%s"%foldername.split("\\")[-1]
  os.system("mkdir %s"%outfolder)

  name=cut[1]
  ID=cut[2]
  if mode=="SLHA":
    if cut[0].upper() != "BLOCK":
      print("Error: because now only suppor block!")
      sys.exit()
    
    for infile in glob.glob( os.path.join(foldername, filename) ):
      #print infile
      val_com = lslha.block(cut[1], cut[2], infile)
      #print val, val_com
      if abs(val - val_com) < eps:
        #print abs(val-val_com)
        os.system("cp %s %s/"%(infile, outfolder))
  
  return outfolder       
