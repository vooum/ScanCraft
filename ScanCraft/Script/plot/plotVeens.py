#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib_venn import venn3

plt.figure(figsize=(10, 10))
v = venn3(subsets=(790,60,772,5,541,6,562),set_labels=('Nsd','Psi','LHC'))
plt.text(-0.5,0.75,'42 higgsino-like N1 points left',fontsize=22)
plt.savefig('h')

plt.figure(figsize=(10, 10))
v = venn3(subsets=(1274,399,1395,16,635,8,636),set_labels=('Nsd','Psi','LHC'))
plt.text(-0.5,0.75,'205 singlino-like N1 points left',fontsize=22)
plt.savefig('s')

plt.figure(figsize=(10, 10))
v = venn3(subsets=(16,114,18,5,5,79,11),set_labels=('Nsd','Psi','LHC'))
plt.text(-0.5,0.75,'27 Bino-like N1 points left',fontsize=22)
plt.savefig('b')