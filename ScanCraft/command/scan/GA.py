#!/usr/bin/env python3

import random,math
import numpy as np
# from hola import matscat




Ctrl=[100,   #0  npop
	  50,	 #1  ngen
	  2,	 #2  nd
	  5,	 #3  nl
	  0.85,  #4  pcross
	  3,	 #5  imut
				#imut=1    Uniform mutation, variable rate based on fitness
				#imut=2    Uniform mutation, variable rate based on distance
				#imut=3    Uniform or creep mutation, variable rate based on fitness
				#imut=4    Uniform or creep mutation, variable rate based on distance
	  0.005, #6  pmut
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
		print('****************************GA Output********************************')
		rk=self.rankpop(self.storage_N)
		# print('Next_storage_0,storage_N:',self.storage_0,'\n',self.storage_N,self.storage_N.shape)
		# print('Next_index:',self.index_x2)
		self.adjmut(self.PopulationN,self.index_x2)
		while i < self.npop/2:
			male=self.select()
			female=self.select()
			while (male == female).all():
				female=self.select()
			em=self.encode(male)
			ef=self.encode(female)
			self.cross(em,ef)
			self.mutation(em)
			self.mutation(ef)
			male=self.decode(em)
			female=self.decode(ef)
			pa=np.array([male,female],dtype=np.float)
			self.genrep(i,pa)
			i+=1
		if self.Judge_InheritElite:
			self.newpop()
		self.Judge_InheritElite=False
		
	
		print('New population:',self.newph)
		print('********************************GA END*********************************')
		return self.newph



	def rankpop(self,storage):      #storage=[[par1,par2...chisq],...]
		rank={}
		self.index_x2={}
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
		self.index={y:x for x,y in rank.items()}  
		return rank

	
	def adjmut(self,phN,chisq,rdiflow=0.05,rdifhi=0.25,delta=1.5):
		best=self.index[1]
		median=self.index[self.npop/2]
		x=phN
		#ajustment based on fitness
		if self.imut == 1 or self.imut == 3 :
			rdif = abs(chisq[best]-chisq[median])\
			     	/(chisq[best]+chisq[median])
			print('ajustment based on fitness')
		#ajustment based on distance
		elif self.imut == 2 or self.imut == 4:
			rdif = 0
			for i in range(self.nd):
				rdif = rdif + (x[best,i]-x[median,i])**2
			rdif = math.sqrt(rdif)/self.nd
			print('ajustment based on distance')
		if rdif <= rdiflow:
			self.pmut=min(self.pmutmx,self.pmut*delta)
		elif rdif >= rdifhi:
			self.pmut= max(self.pmutmn,self.pmut/delta)
		#print('pmute:',self.pmut)


	def select(self):
		self.npop1=self.npop+1
		dice=random.random()*self.npop*self.npop1     #random.random():0<=n<1.0,
		#roulette wheel~rt
		rtfit=0
		i=0
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
		#first point
		cutp1=int(random.random()*self.nl*self.nd)+1
		#one-point crossover
		if random.random()< 0.5:
			cutp2=self.nl*self.nd
		else:
			#second point
			cutp2=int(random.random()*self.nl*self.nd)+1
			#ensure cutp2>cutp1
			if (cutp2 < cutp1):
				tmp=cutp2
				cutp2=cutp1
				cutp1=tmp
		for i in range(cutp1,cutp2):
			t=gn2[i]
			gn2[i]=gn1[i]
			gn1[i]=t
		# print("The cut point is:",cutp1,cutp2)
		# print('after crossover:',gn1,gn2)

	def mutation(self,gn):
		#creep mutation
		if self.imut >= 3 and random.random() < 0.5:
			for i in range(self.nd):
				for j in range(self.nl):
					if random.random() < self.pmut:
						locus=i*self.nl+j
						increase=random.choice([-1,1])
						leftboundary=i*self.nl
						gn[locus]=gn[locus]+increase
						#this is where we carry over the one(up to two digits)
						#first take care of decrement below 0 case
						if increase == -1 and gn[locus] < 0:
							if j == 0 :
								gn[locus]=0
							else:
								for k in range(locus,leftboundary,-1):
									gn[k] = 9
									gn[k-1] = gn[k-1] - 1
									if gn[k-1] >= 0:
										break
								#fix up 00000 case
								if gn[leftboundary] < 0 :
									for l in range(leftboundary,locus+1):
										gn[l] = 0
						#take care of increment beyond 9 case
						elif increase == 1 and gn[locus] > 9:
							if j == 0:
								gn[locus]=9
							else:
								for k in range(locus,leftboundary,-1):		
									gn[k] = 0
									gn[k-1] = gn[k-1] + 1
									if gn[k-1] <= 9 :
										break
								#fix up 99999 case
								if gn[leftboundary]> 9 :
									for l in range(leftboundary,locus+1):
										gn[l] = 9
		#uniform mutation
		else:
			for i in range(self.nl*self.nd):
				if random.random() < self.pmut:
					t=gn[i]
					gn[i]=random.randint(0,9)           #random.randint(a,b):a<=n<=b
					# print('The mutation point of',i,'\n'
					#   'mutation:',t,'-->',gn[i])
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
		# print("before s0 newchisq",newchisq,'\n',newx2_min)
		if self.storage_0==[]:
			pass
		else:
			self.rankpop(self.storage_0)
			oldchisq=self.index_x2
			# print('newchisq,oldchisq:',newchisq,'\n',oldchisq,'\n',self.index[1])
			print('newx2_first,oldx2_min:',newx2_min,oldchisq[self.index[1]])
			if self.ielite==1 and newx2_min > oldchisq[self.index[1]]:
				for i in range(self.nd):
					self.newph[0,i]=self.storage_0[self.index[1],i]




			
			

		
