
#include "../include/micromegas.h"
#include"../include/micromegas_aux.h"
#include "lib/pmodel.h"
#include <string>
#include <iostream>
using namespace std;

template <class T>
int getArrayLen(T& array)
{//使用模板定义一 个函数getArrayLen,该函数将返回数组array的长度
return (sizeof(array) / sizeof(array[0]));
}

int main(int argc, char ** argv)
{
    if(argc<2){
        cout<<"The program needs one argument:the name of SLHA input file.\n"
            <<"Example: ./main spectr.dat"
            <<endl;
        exit(1);
    }
    else{
        cout<<"Initial file: "<<argv[1]<<endl;
    }
// read input file
    int err;
    char cdmName[10];
    int spin2, charge3,cdim;
    //    char lspname[10], nlspname[10];
    int mode = 4;
    /*
    mode= 1*m1+2*m2+4*m4+8*m8+16*m16
    
    m1  0 overwrite all;  1 keep old data
    m2  0 ignore mistake  1: stop in case of mistake in input file.
    m4  0 read DECAY      1: don't read   Decay 
    m8  0 read BLOCK      1: don't read   Blocks
    m16 0 read QNUMBERS   1: don't read   QNUMBERS 
    */
    err=readSLHA(argv[1],mode);
    if(err){
        cout<<"read error, err="<<err<<endl;
        exit(2);
    }
    slhaWarnings(stdout);
    if(err){
        cout<<"error, err="<<err<<endl;
        exit(1);
    }

    err=sortOddParticles(cdmName);
    if(err){cout<<"Can't calculate "<<cdmName<<endl;exit(1);}
    
    qNumbers(cdmName,&spin2, &charge3, &cdim);
    cout<<"\nDark matter candidate is "<<cdmName<<" with spin="<<spin2<<"/2"; 
    if(charge3) { printf("Dark Matter has electric charge %d/3\n",charge3); exit(1);}
    if(cdim!=1) { printf("Dark Matter is a color particle\n"); exit(1);}
    if(strcmp(cdmName,"~o1")) printf(" ~o1 is not CDM\n"); 
    else o1Contents(stdout);

//================= Omega ============================================================
    int fast=1;
    double Beps=1.E-4, cut=0.01;
    double Omega,Xf;
    // to exclude processes with virtual W/Z in DM   annihilation
    VWdecay=1; VZdecay=0; cleanDecayTable();  
    Omega=darkOmega(&Xf,fast,Beps);
    printf("Xf=%.2e Omega=%.2e\n",Xf,Omega);
    if(Omega>0)printChannels(Xf,cut,Beps,1,stdout);
    // FILE* so=fopen("screenout","w");
    // printChannels(Xf,cut,Beps,1,so);
    // to restore default switches  
    VZdecay=1; VWdecay=1; cleanDecayTable();  

//================= Indirect Detection ===============================================
    double Emin=1,/* Energy cut  in GeV   */  sigmaV;
    double vcs_gz,vcs_gg;
    char txt[100];
    double SpA[NZ],SpE[NZ],SpP[NZ];
    double FluxA[NZ],FluxE[NZ],FluxP[NZ];
    //  double * SpNe=NULL,*SpNm=NULL,*SpNl=NULL;
    double SpNe[NZ],SpNm[NZ],SpNl[NZ];
    double Etest=Mcdm/2;

    //sigmaV=calcSpectrum(1+2+4,SpA,SpE,SpP,SpNe,SpNm,SpNl ,&err);
    sigmaV=calcSpectrum(1+2+4,SpA,NULL,NULL,NULL,NULL,NULL ,&err);
    /* Returns sigma*v in cm^3/sec.     SpX - calculated spectra of annihilation.
       Use SpectdNdE(E, SpX) to calculate energy distribution in  1/GeV units.
       
       First parameter 1-includes W/Z polarization
                       2-includes gammas for 2->2+gamma
                       4-print cross sections             
    */
    printf("sigmav=%.2E[cm^3/s]\n",sigmaV);

//================= CDM_NUCLEON =================================================
    double pA0[2],pA5[2],nA0[2],nA5[2];
    double Nmass=0.939; /*nucleon mass*/
    double SCcoeff;

    calcScalarQuarkFF(0.553,18.9,34.,42.);// calcScalarQuarkFF( Mu/Md, Ms/Md, sigmaPiN[MeV], sigma0[MeV])     

    nucleonAmplitudes(CDM1, pA0,pA5,nA0,nA5);
    printf("CDM-nucleon micrOMEGAs amplitudes:\n");
    printf("proton:  SI  %.3E  SD  %.3E\n",pA0[0],pA5[0]);
    printf("neutron: SI  %.3E  SD  %.3E\n",nA0[0],nA5[0]); 

    SCcoeff=4./M_PI*3.8937966E8*pow(Nmass*Mcdm/(Nmass+ Mcdm),2.);
    printf("CDM-nucleon cross sections[pb]:\n");
    printf(" proton  SI %.3E  SD %.3E\n",SCcoeff*pA0[0]*pA0[0],3*SCcoeff*pA5[0]*pA5[0]);
    printf(" neutron SI %.3E  SD %.3E\n",SCcoeff*nA0[0]*nA0[0],3*SCcoeff*nA5[0]*nA5[0]);



//================= output DarkMatter informations ====================================


FILE *Out_Omega=fopen("Omega.txt","w");
fprintf(Out_Omega,"# Input file: %s\n",argv[1]);
{//DMRD
    // omega
    fprintf(Out_Omega,"Block ABUNDANCE\n");
    fprintf(Out_Omega,"%8i%16.8f\t# WIMP mass\n",0,Mcdm);
    fprintf(Out_Omega,"%8i%16.8f\t# relic density omega h^2\n",4,Omega);
    fprintf(Out_Omega,"%8i%16.8f\t# T_f[GeV]\n",1,Mcdm/Xf);
    //fprintf(Out_Omega,"%8i%16.8f\t# T_f[GeV]",3,)
    if(Omega>0)
    {
        fprintf(Out_Omega,"Block ContributeOmega\n");
        printChannels(Xf,cut,Beps,0,Out_Omega);
    }
}
{//Direct Detect
    fprintf(Out_Omega,"Block NDMCROSSSECT\n");
    fprintf(Out_Omega,"%8i%16.8e\t# csPsi [cm^2]\n",1,SCcoeff*pA0[0]*pA0[0]*1e-36);
    fprintf(Out_Omega,"%8i%16.8e\t# csNsi [cm^2]\n",2,SCcoeff*nA0[0]*nA0[0]*1e-36);
    fprintf(Out_Omega,"%8i%16.8e\t# csPsd [cm^2]\n",3,3*SCcoeff*pA5[0]*pA5[0]*1e-36);
    fprintf(Out_Omega,"%8i%16.8e\t# csNsd [cm^2]\n",4,3*SCcoeff*nA5[0]*nA5[0]*1e-36);
}
{//Indirect Detect
    fprintf(Out_Omega,"Block ANNIHILATION\n");
    fprintf(Out_Omega,"%8i%16.8e\t# SigmaV [cm^3/s]\n",0,sigmaV);
    double w_i=0.;
    for(int ii=0; ii<100; ii++)
    {
        w_i=vSigmaCh[ii].weight;
        if (w_i<1e-6)break;
        // cout<<w_i<<endl;
        fprintf(Out_Omega,"%8i%16.8e\t",ii+1,w_i);
        fprintf(Out_Omega,"%s %s -> %s %s",vSigmaCh[ii].prtcl[0],vSigmaCh[ii].prtcl[1],vSigmaCh[ii].prtcl[2],vSigmaCh[ii].prtcl[3]);
        if (vSigmaCh[ii].prtcl[4])fprintf(Out_Omega," %s",vSigmaCh[ii].prtcl[4]);
        fprintf(Out_Omega,"\n");
    }
}
fclose(Out_Omega);

//================= dSphs output E, dN/dE
{
    double E;
    FILE *E_dNdE=fopen("E_dNdE_single.txt","w");
    for(int i=1;i<NZ;i++)
      {
        E=SpA[0]*exp(Zi(i));
        fprintf(E_dNdE,"%e,%e\n",E,SpA[i]/E);
      }
    fclose(E_dNdE);
}
//================= output for GCE chisqure: E^2*dN/dEdOmega of sight toward GC in azimuth angle Omega(see bellow) at E_i ==================================
{
    FILE *GCEin=fopen("emeans.txt","r");
    double Ex[100]={0};
    int ExNum=0;
    while(!feof(GCEin))
    {
        if (ExNum>99) printf("==== Err: The num of ExNum > 100 =======\n");  
        fscanf(GCEin,"%lf",&Ex[ExNum]);
        ExNum++;
    }
    ExNum--;
    fclose(GCEin);

    FILE *FLUXTAB=fopen("EEdN_dEdO_sight.txt","w+");
    const double Deg2Pi = 3.1415926/180.0; // A const translate degree to Pi
    double Omega=(40*Deg2Pi)*(sin(20*Deg2Pi)-sin(2*Deg2Pi)); //Total azimuth angle , L : -20~20 digree; B : 2~20 digree.
    double EEdNdEdO;
    for (int ii=0; ii<ExNum; ii++)
    {
        EEdNdEdO=gammaFluxGC(-20.*Deg2Pi,2.*Deg2Pi,40*Deg2Pi,18*Deg2Pi,sigmaV*SpectdNdE(Ex[ii],SpA))/Omega*Ex[ii]*Ex[ii]; // gammaFluxGC( l, b, dl, db, dsigmaVdE ) * E^2 / Omega
        fprintf(FLUXTAB,"%10.3f%16.4e\n",Ex[ii],EEdNdEdO);
    }
    fclose(FLUXTAB);
}


    return 0;
}