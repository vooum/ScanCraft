#!/usr/bin/env python
# coding: utf-8

# In[2]:


# get_ipython().run_line_magic('matplotlib', 'inline')
# get_ipython().run_line_magic('load_ext', 'autoreload')
# get_ipython().run_line_magic('autoreload', '2')

import sys,os
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')
sys.path.append('/home/vooum/Desktop/ScanCraft/ScanCraft')
sys.path.append('C://Users//vooum//Desktop//ScanCraft//ScanCraft')


from command.scan.scan import scan
from command.nexus.NMSSMTools import NMSSMTools


mold=scan(method="random")
mold.AddScalar('tanB','MINPAR',3,1.,60.)
mold.AddScalar('M1','EXTPAR',1  ,20.    ,1000.)
mold.AddScalar('M2','EXTPAR'   ,2  ,100.    ,2000.)
mold.AddScalar('Atop','EXTPAR'   ,11  ,  -6e3    ,6e3)
mold.AddFollower('Abottom','EXTPAR'   ,12,'Atop')
mold.AddScalar('Atau','EXTPAR'   ,13  ,  100.      ,2000.)
mold.AddFollower('MtauL','EXTPAR'   ,33,'Atau')
mold.AddFollower('MtauR','EXTPAR'   ,36,'Atau')
mold.AddScalar('MQ3L','EXTPAR'   ,43,	100.,	2.e3)
mold.AddScalar('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3)
mold.AddFollower('MbottomR','EXTPAR'  ,49,'MtopR')
mold.AddScalar('Lambda','EXTPAR'  ,61  ,1e-3    ,1. ,prior_distribution='exponential')
mold.AddScalar('Kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,prior_distribution='exponential')
mold.AddScalar('A_Lambda','EXTPAR' ,63,-3.e3,3.e3)
mold.AddScalar('A_kappa','EXTPAR' ,64,-3.e3,3.e3)
mold.AddScalar('mu_eff','EXTPAR'  ,65,100.,1500.)




[k for k in mold.variable_dict.keys()]


# In[28]:


len(_27)


# In[32]:


[k for k in mold.free_parameter_list.keys()]


# In[29]:


mold.Print()


# In[30]:


mold.Sample()


# In[31]:


mold.Print()


# In[39]:


N=NMSSMTools(input_mold="/home/vooum/Desktop/ScanCraft/ScanCraft/packages/NMSSMTools_5.5.2/inpZ3.dat")


# In[41]:


N.Make()


# In[42]:


N.Run(mold)


# In[44]:


N.data_dir


# In[49]:


_42('EXTPAR',1)


# In[50]:


_42.error


# In[ ]:




