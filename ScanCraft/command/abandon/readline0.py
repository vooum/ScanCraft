#!/usr/bin/env python3


read a single line, return a list of the information.
def readline0(line):
  a=line.split()
  if a[0]=='#':a.append(False);a.remove('#')#;print(a);print(a[-1])
  else: a.append(True)
  Ntail=len(a)
  a2=[]
  numF=True
  for i in a[:-1]:
    if '#' in i:
      if i.index('#') >0 : print('annotation wrong in ',line,);exit()
      Ntail=a.index(i)
      break

    for k in i:
      if not k in'0123456789-+.dDEe':numF= False;break
    else:
      if (i.count('.')<2 and 
          i.count('d')+i.count('D')+i.count('E')+i.count('e')<2 and
          (i.count('d')+i.count('D')+i.count('E')+i.count('e')
            +i.count('.')+i.count('+')+i.count('-')<len(i))
         ):  numF=True
      else: numF=False

    if numF:
      i=i.upper()
      if 'D' in i: i=i.replace('D','E')
      if ('E'in i or '.' in i or '+' in i ): i=float(i)#or '-' in i
      else: i=int(i)
    a2.append(i)
  if len(a2)==0: a2=[line[:-1]]
  elif Ntail<len(a): a2.append(' '.join(a[Ntail:-1]))
  a2.append(a[-1])
  return a2
