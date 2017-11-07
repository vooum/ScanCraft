import matplotlib.pyplot as plt
import numpy

def scatter(points, xlabel, ylabel, figname, axlog=[False, False], axlim=[[], []], lines=[]):
  fig=plt.figure()
  fig.patch.set_facecolor("white")
  ax=fig.add_axes([0.14, 0.12, 0.8, 0.8])

  set_legend=False

  group_scatter=[]
  label_scatter=[]
  if len(points) != 0:
    for pair in points:
      im=ax.scatter(pair[0], pair[1], s=pair[2], marker=pair[3], c=pair[4], edgecolor="face")
      group_scatter.append(im)
      label_scatter.append(pair[5])

    if points[0][5] != None:
      set_legend = True

  ax.set_xlabel(r"%s"%xlabel, fontsize=16)
  ax.set_ylabel(r"%s"%ylabel, fontsize=16)
 
  #ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
  if len(axlog) != 0:
    if axlog[0]:
      ax.set_xscale('log')
    if axlog[1]:
      ax.set_yscale('log')
  if len(axlim) !=0 :
    if len(axlim[0]) != 0:
      ax.set_xlim(axlim[0][0], axlim[0][1])
    if len(axlim[1]) != 0:
      ax.set_ylim(axlim[1][0], axlim[1][1])

  group_line = []
  label_line = []
  if len(lines) != 0:
    set_legend=True
    for line in lines:
      l, = ax.plot(line[0], line[1], line[2])
      group_line.append(l)
      label_line.append(line[3])

#legend(loc='best', ...) works 99%
#More info by google "test if legend is covering any data"
  if set_legend:
    ax.legend(group_scatter+group_line, label_scatter+label_line, loc="best", ncol=3, fontsize=10, numpoints=1, scatterpoints=1)

  plt.savefig("%s.png"%figname)

def scatter_color(x,y,z, xlabel, ylabel, zlabel, figname, axlog=[False, False], axlim=[[], []], zformat="%5.2E", lines=[]):
  fig=plt.figure()
  fig.patch.set_facecolor("white")
  ax=fig.add_axes([0.15, 0.12, 0.68, 0.8])
  im=ax.scatter(x,y, c=z, marker="o", s=10, edgecolor="face", cmap=plt.cm.cool)
  ax.set_xlabel(r"%s"%xlabel, fontsize=16)
  ax.set_ylabel(r"%s"%ylabel, fontsize=16)

  if len(axlog) != 0:
    if axlog[0]:
      ax.set_xscale('log')
    if axlog[1]:
      ax.set_yscale('log')
  if len(axlim) !=0 :
    if len(axlim[0]) != 0:
      ax.set_xlim(axlim[0][0], axlim[0][1])
    if len(axlim[1]) != 0:
      ax.set_ylim(axlim[1][0], axlim[1][1])

  cbar_ax=fig.add_axes([0.84, 0.12, 0.03, 0.8])
  ts=numpy.linspace(numpy.amin(z), numpy.amax(z), 6, endpoint=True)
  fig.colorbar(im, cax=cbar_ax, orientation="vertical", ticks=ts, format=zformat)
  cbar_ax.tick_params(axis="y", direction="in", labelsize="medium", pad=5)
  cbar_ax.xaxis.set_label_text(r"%s"%zlabel)
  cbar_ax.xaxis.set_label_position("top")

  if len(lines) != 0:
    for line in lines:
      l = ax.plot(line[0], line[1], line[2], label=line[3])
    #legend(loc='best', ...) works 99%
    #More info by google "test if legend is covering any data"
    ax.legend(loc="best", ncol=3, fontsize=10, numpoints=1)

  plt.savefig("%s.png"%figname)
