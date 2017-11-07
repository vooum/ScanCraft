import sys

def block(name, ID, filename):
  ID=map(int, ID.split())
  if len(ID)==1:
    mode="item"
  elif len(ID)==2:
    mode="matrix"
  else:
    print("Error: because only support item or matrix mode!")
    sys.exit(1)

  with open(filename, "r") as f:
    lines = f.readlines()
    find_block=0
    for line in lines:
      words=line.split()
      if len(words)==0:
        continue
      elif words[0]=="#":
        continue
      elif words[0].upper()=="BLOCK":
        if words[1].upper()==name.upper():
          find_block = 1
      else:
        if find_block:
          if mode=="item":
            if int(words[0])==ID[0]:
              return float(words[1])
          elif mode=="matrix":
            if ID[0]==int(words[0]) and ID[1]==int(words[1]):
              return float(words[2])

  print("Error: could not find specified item in slha file!")
  sys.exit()
