#!/usr/bin/env python3

from matplotlib import pyplot as plt
import matplotlib as mpl

fig=plt.figure(figsize=(10, 0.8))# Bar ======
ax3 = fig.add_axes([0.05, 0.5, 0.9, 0.45])
cmap=mpl.colors.ListedColormap(['k','y','b','r'])
bounds=[0,772,832,1622,1664]
norm=mpl.colors.BoundaryNorm(bounds,cmap.N)
bar=mpl.colorbar.ColorbarBase(ax3,cmap=cmap,
                              norm=norm,
                              ticks=None,
                              spacing=[772,832,1622,1664],
                              orientation='horizontal')
bar.set_ticks([300,802,1227,1643])
bar.set_ticklabels(['excluded by $\sigma^{SD}_{\widetilde{\chi}-n}$ and $\sigma^{SI}_{\widetilde{\chi}-p,2016}$'
                    ,'excluded by $\sigma^{SI}_{\widetilde{\chi}-p,2016}$'
                    ,'excluded by $\sigma^{SD}_{\widetilde{\chi}-n}$'
                    ,'survived'])
fig.savefig('h_exclude_bar')