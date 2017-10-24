#!/usr/bin/python3

import sys,os,re,copy,shutil
print(sys.argv)

if len(sys.argv)==1:
  DataSteam='mcmc/'
else:
  DataSteam=sys.argv[1]
RecordDir = os.path.join(DataSteam,'')
if not os.path.exists(RecordDir): exit('Directory '+ DataSteam +' not exist')

if len(sys.argv)==3:
  OutSteam=sys.argv[2]
else:
  OutSteam='Analysed'
if os.path.exists(OutSteam):exit('Directory '+ OutSteam +' already exist')
os.mkdir(OutSteam)
print(RecordDir)

#-------------- get all spectr and omega files
spectrs=[]
omegas=[]
for name in os.listdir(RecordDir):
  nameDir=os.path.join(RecordDir,name)
  if 'spectr' in name and os.path.isfile(nameDir) and 'from' not in name:
    spectrs.append(nameDir)
  if 'omega' in name and os.path.isfile(nameDir):
    omegas.append(nameDir)
#    print(fileDir)
spectrs.sort(key=lambda x: int(re.findall(r'\d+',x)[-1]))
omegas.sort(key=lambda x: int(re.findall(r'\d+',x)[-1]))

# Functions ---------------------------------------------------------
def chi2(mu, data): #     chisq_mh = chi2(value_mh,mh)
    return (mu-data[0])**2/(data[1]**2+data[2]**2)
mh =[125.7, 0.4, 1.5]
bsg=[3.43, 0.21, 0.3]
bmu=[2.9, 0.7, 0.38]
omg=[0.1187,0.0017,0.012]
gm2=[28.7,8.0,2.0]
def readline(line):
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
          (i.count('d')+i.count('D')+i.count('E')+i.count('e')+i.count('.')+i.count('+')+i.count('-')<len(i))
         ):  numF=True
      else: numF=False

    if numF:
      i=i.upper()
      if 'D' in i: i=i.replace('D','E')
      if ('E'in i or '.' in i or '+' in i or '-' in i): i=float(i)
      else: i=int(i)
#      print(i.find('d'),i.count('d'),i)
    a2.append(i)
  if len(a2)==0: a2=[line[:-1]]
  elif not a[-1] and type(a2[0])==type('a'): a2=[line[:-1]]
  elif Ntail<len(a): a2.append(' '.join(a[Ntail:-1]))
  a2.append(a[-1])
#  print(a)
  return a2

Allpar=open(os.path.join(OutSteam,'AllParameters.txt'),'w')
#-----------------------------------------------
for files in spectrs:
  spectr=open(files,'r').readlines()
#--------- get quantities ---------------------------
  BLOCK=''
  DECAY=[]
  Mh={}
  Mh_n={25:'h1',35:'h2',45:'h3',36:'A1',46:'A2',37:'Ch'}
  Msp={}
  Msp_n={1000022:'N1',1000023:'N2',1000025:'N3',1000035:'N4',1000045:'N5',1000024:'C1',1000037:'C2'}
  Hcouplings={}
  Hmix={}
  Nmix={}
  chisq_Q={}
  brHAA=1e-10
  brAgg=1e-10
  H2cs,H3cs=0.,0.
  DM=0.1181
  HBresult=1
  HSresult=1.
  parameters={}.fromkeys((0	# tanBeta
  			 ,1	# M1
  			 ,2	# M2
  			 ,3	# M3
  			 ,11	# At
  			 ,12	# Ab
  			 ,13	# AE3
  			 ,16	# AE2
  			 ,32	# ML2
  			 ,33	# ML3
  			 ,35	# ME2
  			 ,36	# ME3
  			 ,42	# MQ2
			 ,43	# MQ3
			 ,45	# MU2
			 ,46	# Mt3
			 ,48	# MD2
			 ,49	# Mb3
			 ,61	# L
			 ,62	# K
			 ,63	# Al
			 ,64	# Ak
			 ,65	# mu
#			 ,66	# xif
#			 ,67	# xis
#			 ,68	# mu'
#			 ,69	# Ms'**2
#			 ,70	# mu for Z3 break
#			 ,72	# M3H**2
			 ,124	# MA
			 ,125	# MP))
			 ),0.
			)
  BrSb={}.fromkeys(('C1_N1_mu_v'
		 ,'N2_N1_h1'
		 ,'N3_N1_h1'
		 ,'N4_N1_h1'
		 ),0.
		)




  for line in spectr:
    a=readline(line)
#    if not a[-1]: continueparameters
    if type(a[0])==type('1'):
      if a[0].upper()=='DECAY':BLOCK=''; DECAY=copy.deepcopy(a);continue
      if a[0].upper()=='BLOCK':BLOCK=a[1];DECAY=[];continue
    elif BLOCK== 'SPINFO':
      if a[0] == 4: print(files,line[:-1]); break
      if a[0] == 3: print(files,line[:-1]);break
    elif BLOCK=='MINPAR':
      if   a[0] == 3 : parameters[0]=a[1]
    elif BLOCK=='EXTPAR':
      if a[0] in parameters.keys():
        parameters[a[0]]=a[1]
    elif BLOCK=='MASS':
      if   a[0] in Mh_n.keys(): Mh['M_'+Mh_n[a[0]]]=a[1]
      elif a[0] in Msp_n.keys(): Msp['X_'+Msp_n[a[0]]]=a[1]
#      if a[0] == 
#    elif BLOCK=='EXTPAR':
#      if a[0] == 125:		chisq_Q['MP'] =a[1]**2/100.
    elif BLOCK  =='LOWEN':
      if   a[0] == 1:		chisq_Q['bsg']=chi2(a[1]*1.e4,bsg)
      elif a[0] == 4:		chisq_Q['bmu']=chi2(a[1]*1.e9,bmu)
      elif a[0] ==10:	DM=a[1]
    elif BLOCK  =='REDCOUP':
      Hcouplings[tuple(a[:2])]=a[2]
    elif BLOCK  =='NMHMIX':
      Hmix[tuple(a[:2])]=a[2]
    elif BLOCK  =='NMNMIX':
      Nmix[tuple(a[:2])]=a[2]
    elif DECAY!=[]:
      if   DECAY[1]==36:
        if a[1:4]==[2,22,22]:brAgg=a[0]
      elif DECAY[1]==35:
        if a[1:4]==[2,36,36]:brH2AA=a[0]
      elif DECAY[1]==45:
        if a[1:4]==[2,36,36]:brH3AA=a[0]
      elif DECAY[1]==1000024:
        if a[1:5]==[3,1000022,-13,14]:BrSb['C1_N1_mu_v']=a[0]
      elif DECAY[1]==1000023:
        if a[1:4]==[2,1000022,25]:BrSb['N2_N1_h1']=a[0]
      elif DECAY[1]==1000025:
        if a[1:4]==[2,1000022,25]:BrSb['N3_N1_h1']=a[0]
      elif DECAY[1]==1000035:
        if a[1:4]==[2,1000022,25]:BrSb['N4_N1_h1']=a[0]
    elif BLOCK  =='HiggsBoundsResults':
      if a[0]==1:
        if a[1]==2:
          HBresult=a[2]
    elif BLOCK  =='HiggsSignalsResults':
      if a[0]==13:
        HSresult=a[1]


  else:

    if HBresult!=1 or HSresult<0.05:continue
    
    Number=re.findall(r'\d+',files)[-1]
    if int(Number)%100==0: print(Number,' points read')
#    Allpar.write('AA: '+str(AA)+' BrAgg: '+str(brAgg)+' bbrr: '+str(bbrr)+'\t')
    All25Parameters=[parameters[i] for i in [61,62,0 ,65,63
					    ,64,43,46,49,33
					    ,36,11,12,13,42
					    ,45,48,32,35,1
					    ,2 ,3 ,124,125,16
					    ]
    		    ]
    for i in [7,8,9,10,11,15,16,17,18,19]:
      All25Parameters[i-1]=All25Parameters[i-1]**2
    Allpar.write(Number+'\t')
    Allpar.write('\t'.join([str(i) for i in All25Parameters]))
    Allpar.write('\n')
print('All spectr files recorded')

