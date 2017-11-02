#Helpful info for control types of line
#line: "-", "--", "-.", ":", "."
#color: "b", "g", "r", "c", "m", "y", "k", "w"
#marker: "None", " ", or ""
#marker: "o", "*"

#Helpful info for using "numpy" 
#numpy: "and" should be "&", "or" should be "|".
import sys
import os
import numpy

sys.path.append("%s/liangbin/"%os.environ["HOME"])
import lread
import lplot

#start of dealing data
#data=lread.read("ScanInf.txt", "READData.txt", [], 1)
data=lread.read("ScanInf.txt", "MCMCData.txt", [], 1)
#sel initial
if len(data.dtype.names) != len(set(data.dtype.names)):
  print "Error: Duplicate names of column in data!"
  sys.exit()

print ">>>>>>>> support column name in data <<<<<<<<<\n"
print data.dtype.names
print "\n=============================================="

sel=(\
    (data["BRB0_smumu"]>1.72e-9) & (data["BRB0_smumu"]<4.5e-9) & \
    (data["LSP_pdg"]==4000012.) & \
    (data["omega"]>0.107) & (data["omega"]<0.131) & \
    (data["hh_1"]>122.1) & (data["hh_1"] < 128.1) & \
    (data["BRBX_sgamma"]>2.99e-4) & (data["BRBX_sgamma"]<3.87e-4) & \
    (data["Cha_2"]>103.5) & \
    (data["Cha_1"]>103.5) & \
    (data["HBresult"]==1) & \
    (data["Pvalue"]>0.05) \
)
print sel

#sel specify
interp_1data=numpy.genfromtxt("XENON1T.dat")
interp_1x=interp_1data[:,0]
interp_1y=numpy.log10(interp_1data[:,1]*1E-09)
sel_cut1=numpy.log10(data["proton_si"]) < numpy.interp(data["SvIm_1"], interp_1x, interp_1y)

sel_cut2=data["Fermi_Lat"]<1.355

#sel combine
sel_01=sel & numpy.logical_not(sel_cut1) & numpy.logical_not(sel_cut2)
sel_02=sel & sel_cut1                    & numpy.logical_not(sel_cut2)
sel_03=sel & numpy.logical_not(sel_cut1) & sel_cut2
sel_04=sel & sel_cut1                    & sel_cut2

#sel shown in number
x=data["SvIm_1"]
print "\n=============================================="
print "All points=%d, Remain points initial=%d, afterAll=%d"%(len(x), len(x[sel]), len(x[sel_04]) )

#2d
xlabel=r"$m_{\tilde{\nu}}$"
ylabel="$\sigma_{SI} (cm^2)$"
figname="svim_1-proton_si"
x=data["SvIm_1"]
y=data["proton_si"]*10E-36

x1=x[sel_01]
y1=y[sel_01]
size1=10
marker1="o"
color1="r"
label1="Exclude"

x2=x[sel_02]
y2=y[sel_02]
size2=10
marker2="o"
color2="g"
label2="Direct"

x3=x[sel_03]
y3=y[sel_03]
size3=10
marker3="o"
color3="b"
label3="InDir"

x4=x[sel_04]
y4=y[sel_04]
size4=10
marker4="o"
color4="k"
label4="Allow"

points=[[x1,y1,size1,marker1,color1,label1],\
        [x2,y2,size2,marker2,color2,label2],\
        [x3,y3,size3,marker3,color3,label3],\
        [x4,y4,size4,marker4,color4,label4]\
  ]

lplot.scatter(points, xlabel, ylabel, figname, axlog=[False, True], axlim=[[],[1E-55, 1E-41]])

#2d with line
xlabel=r"$m_{\tilde{\nu}}$"
ylabel="$\sigma_{SI} (cm^2)$"
figname="svim_1-proton_si+LINE"
x=data["SvIm_1"]
y=data["proton_si"]*10E-36

x1=x[sel_01]
y1=y[sel_01]
size1=10
marker1="o"
color1="r"
label1="Exclude"

x2=x[sel_02]
y2=y[sel_02]
size2=10
marker2="o"
color2="g"
label2="Direct"

x3=x[sel_03]
y3=y[sel_03]
size3=10
marker3="o"
color3="b"
label3="InDir"

x4=x[sel_04]
y4=y[sel_04]
size4=10
marker4="o"
color4="k"
label4="Allow"

points=[[x1,y1,size1,marker1,color1,label1],\
        [x2,y2,size2,marker2,color2,label2],\
        [x3,y3,size3,marker3,color3,label3],\
        [x4,y4,size4,marker4,color4,label4]\
  ]

line1data=numpy.genfromtxt("LUXlimits2015.dat")
line2data=numpy.genfromtxt("LUXlimits2016.dat")
line3data=numpy.genfromtxt("XENON1T.dat")
l1x=line1data[:,0]; l1y=line1data[:,1]*10E-36;
l2x=line2data[:,0]; l2y=line2data[:,1]*10E-36;
l3x=line3data[:,0]; l3y=line3data[:,1]*10E-45;
lines=[[l1x, l1y, "c-", "LUX2015"], [l2x, l2y, "k-", "LUX2016"],\
       [l3x, l3y, "r-", "XENON1T"]]

lplot.scatter(points, xlabel, ylabel, figname, axlog=[False, True], axlim=[[20, 120], [1E-55, 1E-41]], lines=lines)

#3d
x=data["LAMN_33"]
y=data["alamn_33"]
z=data["omega"]
xlabel="$\lambda_N$"
ylabel="$A_{\lambda_N}$"
zlabel="$\Omega h^2$"
figname="lamn-alamn-omega"
lplot.scatter_color(x, y, z, xlabel, ylabel, zlabel, figname)

#3d with line
x=data["LAMN_33"]
y=data["alamn_33"]
z=data["omega"]
xlabel="$\lambda_N$"
ylabel="$A_{\lambda_N}$"
zlabel="$\Omega h^2$"
figname="lamn-alamn-omega+LINE"

line1data=numpy.genfromtxt("line3data.txt")
line2data=numpy.genfromtxt("line4data.txt")
l1x=line1data[:,0]; l1y=line1data[:,1];
l2x=line2data[:,0]; l2y=line2data[:,1];
lines=[[l1x, l1y, "c-", "line1"], [l2x, l2y, "k-", "line2"]]

lplot.scatter_color(x, y, z, xlabel, ylabel, zlabel, figname, lines)
