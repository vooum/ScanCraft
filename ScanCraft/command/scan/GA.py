#!/usr/bin/env python3

import random
import numpy as np
# from hola import matscat




Ctrl=[100,   #0  npop
	  50,	 #1  ngen
	  14,	 #2  nd
	  5,	 #3  nl
	  0.85,  #4  pcross
	  2,	 #5  imut
	  0.05, #6  pmut
	  0.0005,#7  pmutmn
	  0.25,	 #8  pmutmx
	  0.5,	 #9  fdif  fit级差
	  1,	 #10 irep
	  1,	 #11 ielite
	  0]	 #12 irvb

class ga():
	
	def __init__(self,ctrl=Ctrl):
		self.npop=ctrl[0]
		self.nd=ctrl[2]
		self.nl=ctrl[3]
		self.ngen=ctrl[1]
		self.pcross=ctrl[4]
		self.fdif=ctrl[9]
		self.ielite=ctrl[11]
		self.imut=ctrl[5]
		self.pmut=ctrl[6]
		self.pmutmn=ctrl[7]
		self.pmutmx=ctrl[8]
		self.irep=ctrl[10]
		self.index={}
		self.index_x2={}
		


		self.storage_0=[]
		self.storage_N=[]
		self.PopulationN=[]
		self.newph=np.random.rand(self.npop,self.nd)
		self.Judge_InheritElite=True



	def Generation_new(self,storageN):
		self.storage_0=self.storage_N
		# print('new_storage_0:',self.storage_0)
		self.storage_N=storageN
		self.PopulationN=self.storage_N[:,:self.nd]
		self.Judge_InheritElite=True
		
		

	def Generation_Next(self):
		i=0
		rk=self.rankpop(self.storage_N)
		# print('Next_storage_0,storage_N:',self.storage_0,'\n',self.storage_N)
		# print('Next_index:',self.index_x2)
		self.adjmut(self.index_x2)
		while i < self.npop/2:
			male=self.select()
			female=self.select()
			while (male == female).all():
				female=self.select()
			em=self.encode(male)
			ef=self.encode(female)
			# print(em,ef)
			self.cross(em,ef)
			# print(em,ef,'\n')
			self.mutation(em)
			# print(em)
			self.mutation(ef)
			# print(em,ef)
			male=self.decode(em)
			female=self.decode(ef)
			pa=np.array([male,female],dtype=np.float)
			self.genrep(i,pa)
			i+=1
		if self.Judge_InheritElite:
			self.newpop()
		self.Judge_InheritElite=False

		# print('New population:',self.newph)
		return self.newph



	def rankpop(self,storage):      #storage=[[par1,par2...chisq],...]
		rank={}
		x2=storage[:,self.nd]
		n=0
		for x in x2:
			self.index_x2[n] = x
			n+=1
		irk=1
		x2_sort=sorted(self.index_x2.items(),key=lambda x:x[1])
		for i in x2_sort:
			rank[i[0]]=irk
			irk+=1
		self.index={y:x for x,y in rank.items()}   #根据评级指标得到种群某个体原来的代号，例如第1名原来的代号是5：self.index[1]=5
		return rank

	def select(self):
		self.npop1=self.npop+1
		dice=random.random()*self.npop*self.npop1     #random.random():0<=n<1.0,
		#roulette wheel~rt
		rtfit=0
		i=0
		# print('select_PopulationN:',self.PopulationN.shape)
		while i < self.npop:
			rtfit=rtfit+self.npop1+self.fdif*(self.npop1-2*self.rankpop(self.storage_N)[i])
			# print(rtfit)
			if rtfit >= dice:
				idad = self.PopulationN[i]
				break
			i+=1
		# print('idad:',idad)
		return idad

	def encode(self,ph):
		z=10**self.nl
		gn=[0]*self.nl*self.nd
		ii=0
		for i in ph:
			ip=int(i*z)
			for j in range(self.nl,0,-1):
				gn[ii+j-1]=int(ip%10)
				# print(gn)
				ip=ip/10
			ii+=self.nl
		# print('ph:',ph,'gn:',gn)
		return gn

	def decode(self,gn):
		z=10**(-self.nl)
		ii=0
		ph=[]
		for i in range(self.nd):
			ip=0
			for j in range(self.nl*i,self.nl*(i+1)):
				ip=ip*10+gn[j]
				# print(ip)
			ph.append(ip*z)
		# print('ph:',ph)
		return ph

	def cross(self,gn1,gn2):
		if random.random()<=self.pcross:
			self.cutp=int(random.random()*self.nl*self.nd)+1
			for i in range(self.cutp,self.nl*self.nd):
				t=gn2[i]
				gn2[i]=gn1[i]
				gn1[i]=t
			# print("The cut point is:",self.cutp)
		# else:print("No cross hanppens")

	def mutation(self,gn):
		for i in range(self.nl*self.nd):
			if random.random()<=self.pmut:
				t=gn[i]
				gn[i]=random.randint(0,9)           #random.randint(a,b):a<=n<=b
				# print('The mutation point of',i,'\n'
					  # 'mutation:',t,'-->',gn[i])
		return gn

	def genrep(self,ip,parent):
		ip1=ip*2
		ip2=ip1+1
		for i in range(self.nd):
			self.newph[ip1,i]=parent[0,i]
			self.newph[ip2,i]=parent[1,i]
		 

	def newpop(self):
		newchisq=self.index_x2
		newx2_min=newchisq[0]
		if self.storage_0==[]:
			pass
		else:
			# x2_old=self.storage_0[:,self.nd]
			# n=0
			# for x in x2_old:
			# 	oldchisq[n] = x
			# 	n+=1
			self.rankpop(self.storage_0)
			oldchisq=self.index_x2
			# print('newpop_storage_0:',self.storage_0)
			# print('newchisq,oldchisq:',newchisq,'\n',oldchisq,'\n',self.index[1])
			print('newx2_first,oldx2_min:',newx2_min,oldchisq[self.index[1]])
			if self.ielite==1 and newx2_min > oldchisq[self.index[1]]:
				for i in range(self.nd):
					self.newph[0,i]=self.storage_0[self.index[1],i]
		

	def adjmut(self,chisq,rdiflow=0.05,rdifhi=0.25,delta=1.5):
		rdif=abs(chisq[self.index[1]]-chisq[self.index[self.npop/2]])\
			      /(chisq[self.index[1]]+chisq[self.index[self.npop/2]])
		if rdif <= rdiflow:
			self.pmut=min(self.pmutmx,self.pmut*delta)
		elif rdif >= rdifhi:
			self.pmut= max(self.pmutmn,self.pmut/delta)
		



			
			

		
