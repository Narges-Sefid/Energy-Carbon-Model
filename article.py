# -*- coding: utf-8 -*-
"""Article.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/191Vk_5h43fPZTqqQnXced5-RmF7eTO7R

Mixed Integer Linear Optimization
"""

import numpy as np

#Base Scenario

#Energy Use
E=[[60768487.25,2473742.8],[26963615.92,22297056.42]] #GJ(bof(th,e),dri(th,e))

EEAF=[[296798.0271,52516.8],[292519.0962,78357.59881],[254062.717,43958.73442],
      [163767.294,24672.6972],[27356.32222,2188.8],[166722.5128,26357.8536],
      [154908.7332,29322.8136],[27123.08162,3387.24],[122205.279,64962],
      [333160.3996,14155.2],[33489.56358,7059.636],[40381.39374,7552.9512],
      [136995.467,25149.1716],[171076.4752,18555.8076],[63496.00464,7426.377936],
      [62434.47957,4055.456772],[177115.3385,41259.1392],[93474.03,11725.7508],
      [120612.4372,30891.3876],[253983.5807,44264.5488],[104086.2747,27962.784],
      [13944653.58,3992571.407],[223124.9584,25197.8184],[30116.22992,2408.706],
      [146082.0243,1109430.914],[22922.4916,2308.6296],[639343.3818,86244.2568]]

EBOF=[[60754138.21,2404719936],[14349.3808,69022.8612]] #GJ(U1(th,e),U2(th,e))

#Steel Production
tEAF=[176443.21,182137,150768,107724,13985,146048.7,135577.3,11800,71961.137,
      154160.591,18080.71,56357.125,68466,10000,21448,5299.1,107186,21868.003,
      86319,83393.55,103016,2570910,212440,5464,621217,6400,535152] #Ton
tBOF=[2534367.07,286995] #Ton

#Constants

#Emission Factors
EF=[0.059,0.1835] #(Ton/GJ)(th,E)

#Carbon Emissions
EM=np.array(E)
EFM=np.array(EF)
CE=EM*EFM
CEEEAF=np.array(EEAF)*EFM
CEEBOF=np.array(EBOF)*EFM

CEEEAFT=dict()
for x in range(len(CEEEAF)):
  CEEEAFT[x]=CEEEAF[x][0]+CEEEAF[x][1]

CEEBOFT=dict()
for y in range(len(CEEBOF)):
  CEEBOFT[y]=CEEBOF[y][0]+CEEBOF[y][1]


#Carbon Cost
CPr=29 #($/Ton)
CPrt=CE*CPr

#Energy Cost
Pr=[1320,767] #th(Rial/M3)&e(Rial/kwh)
PrRPGJ=[41483.34,213055.56]
PrRPGJM=np.array(PrRPGJ)
PrDolPGJ=[0.98769857,5.07275]
EC=EM*PrRPGJM #Rial
ECM=np.array(EC)


#Scenario 1(Energy Conservatio Scenario-ECS)

#Technology Description

ECSAC={'CGIBF':2340000,'WPIBF':2340000,'PSP':16480000,'CHP':32960000,'IOPDK':14140000,'SP':14140000} #Application Capacity
ECSEth={'CGIBF':0.36,'WPIBF':0.11,'PSP':0.12,'CHP':0.03,'IOPDK':1.44,'SP':0} #GJ/ton #Thermal Energy Conservation Potential
ECSEekwh={'CGIBF':18.5,'WPIBF':0,'PSP':0,'CHP':97.2,'IOPDK':0,'SP':61.11} #kwh/ton #Electrical Energy Conservation Potential
ECSCapI={'CGIBF':5.92,'WPIBF':0,'PSP':0,'CHP':20.2,'IOPDK':212.3,'SP':7.62} #$/ton #Capital Investment
ECSAnn={'CGIBF':0,'WPIBF':1.44,'PSP':3.176,'CHP':0,'IOPDK':0,'SP':0} #4/ton #Annualized Investment
ECSCI={'CGIBF':1446.5,'WPIBF':1566.9,'PSP':1566.9,'CHP':1566.9,'IOPDK':1446.5,'SP':1566.9} #Cost Index(Reference?)
ECSCIorigin=1593.7


#Dictionary Definitions

ECSE=dict()
ECSAnnCap=dict()
ECSEeGJ=dict()
ECSCPth=dict()
ECSCPe=dict()
ECSAvCstth=dict() #Dollar/ton
ECSAvCste=dict() #Dollar/ton 
ECSAvCsttot=dict() #Dollar/ton
ECSTotI=dict() #Dollar/ton
ECSTotI2017=dict() #Dollar/ton
ECSPP=dict() #years
ECSEcEf=dict() #Dollar/tonCO2
ECSCPtot=dict() #tonCO2
ECSMAC=dict() #Dollar/tonCO2

#Constants

ECSEtotS=0
ECSCPtotS=0
ECSItotS=0
ECSAvCsttotS=0

#Function Definitions

def PaybackPeriod(TotI,AvCsttot):
  PP=TotI/AvCsttot
  return PP

def EcoEfficiency(TotI,AvCsttot,CP):
  EcEf=((AvCsttot*20)-TotI)/CP
  return EcEf

def MarginalAbatementCost(TotI,CP):
  MAC=TotI/CP
  return MAC

#Technology Calculations for Scenario 1

for i in ECSEth:
#Energy Conservation
  ECSEeGJ[i]=ECSEekwh[i]*0.0036
  ECSE[i]=ECSEth[i]+ECSEeGJ[i]

#Carbon Abatement Potential
  ECSCPth[i]=ECSEth[i]*EF[0]
  ECSCPe[i]=ECSEeGJ[i]*EF[1]
  ECSCPtot[i]=ECSCPth[i]+ECSCPe[i]

#Avoided Cost
  ECSAvCstth[i]=ECSEth[i]*PrDolPGJ[0]
  ECSAvCste[i]=ECSEeGJ[i]*PrDolPGJ[1]
  ECSAvCsttot[i]=(ECSAvCstth[i]+ECSAvCste[i])

#Total Investment
  ECSAnnCap[i]=ECSAnn[i]*((((1+0.06)**20)-1)/(0.06*((0.06+1)**20)))
  ECSTotI[i]=ECSCapI[i]+ECSAnnCap[i]

#Technology Cost in 2017
  ECSTotI2017[i]=ECSTotI[i]*ECSCIorigin/ECSCI[i]

#Payback Period
  ECSPP[i]=PaybackPeriod(ECSTotI2017[i],ECSAvCsttot[i])

#Eco-Efficiency
  ECSEcEf[i]=EcoEfficiency(ECSTotI2017[i],ECSAvCsttot[i],ECSCPtot[i])

#Marginal Abatement Cost
  ECSMAC[i]=MarginalAbatementCost(ECSTotI2017[i],ECSCPtot[i])

#Scenario Calculations
  ECSEtotS=ECSEtotS+(ECSE[i]*ECSAC[i])
  ECSCPtotS=ECSCPtotS+(ECSCPtot[i]*ECSAC[i])
  ECSItotS=ECSItotS+(ECSTotI2017[i]*ECSAC[i])
  ECSAvCsttotS=ECSAvCsttotS+(ECSAvCsttot[i]*ECSAC[i])

ECSPPS=PaybackPeriod(ECSItotS,ECSAvCsttotS)
ECSEcEfS=EcoEfficiency(ECSItotS,ECSAvCsttotS,ECSCPtotS)
ECSMACS=MarginalAbatementCost(ECSItotS,ECSCPtotS)


#Scenario 2(Carbon Utilization Scenario-CUS)

#Technology Description
#Carbon Utilization Potential
CUSPC={'CO2TOM':440000,'CO2TOBD':36000} #ton #Production Capacity
CUSPR={'CO2TOM':0.68,'CO2TOBD':0.11} #Product to CO2 Ratio
PrPr={'CO2TOM':476.1904762,'CO2TOBD':1082.25} # Dollar/ton product #Product's Price
CUSOP={'CO2TOM':335,'CO2TOBD':83} #Dollar/ton product #Operational Costs
CUSCI={'CO2TOM':236000000,'CO2TOBD':37422000} #Dollar #Capital Investment

#Capacity Calculation
CO2TOM=0
CO2TOBD=0
x=0
y=0
a=0
b=0

for unit in CEEEAFT:
  x=CEEEAFT[unit]//CUSPC['CO2TOM']
  CO2TOM=CO2TOM+x
  y=(CEEEAFT[unit]%CUSPC['CO2TOM'])//CUSPC['CO2TOBD']
  CO2TOBD=CO2TOBD+y


for unit in CEEBOFT:
  a=CEEBOFT[unit]//CUSPC['CO2TOM']
  CO2TOM=CO2TOM+a
  b=(CEEBOFT[unit]%CUSPC['CO2TOM'])//CUSPC['CO2TOBD']
  CO2TOBD=CO2TOBD+b


#??From here, I make an assumption for the CUS technology capacities and go on with that, instead of calculated amounts in the last piece of code.

CUSCPCT={'CO2TOM':4,'CO2TOBD':3} #units #Applied Capacity

#definitions
CUSCPtot=dict()
CUSCIF=dict()
CUSAnn=dict()
CUSAvCst=dict()
CUSACF=dict()
CUSPP=dict()
CUSEcEf=dict()
CUSMAC=dict()
CUSCPtotS=0
CUSACFS=0
CUSAvCstS=0

#Technology Calculations for Scenario 2
for tech in CUSCPCT:

#Carbon Abatement Potential
  CUSCPtot[tech]=CUSCPCT[tech]*CUSPC[tech]/CUSPR[tech]

#Capital Investment
  CUSCIF[tech]=CUSCI[tech]*CUSCPCT[tech]

#Operational Cost(Annual)
  CUSAnn[tech]=CUSCPCT[tech]*CUSOP[tech]*CUSPC[tech]

#Avoided Cost(Annual)
  CUSAvCst[tech]=CUSCPCT[tech]*PrPr[tech]*CUSPC[tech]

#Annual Cash flow
  CUSACF[tech]=CUSAvCst[tech]-CUSAnn[tech]

#Payback Period
  CUSPP[tech]=PaybackPeriod(CUSCIF[tech],CUSACF[tech])

#Eco-Efficiency
  CUSEcEf[tech]=EcoEfficiency(CUSCIF[tech],CUSACF[tech],CUSCPtot[tech])

#Marginal Abatement Cost
  CUSMAC[tech]=MarginalAbatementCost(CUSCIF[tech],CUSCPtot[tech])

#Scenario Calculations
  CUSCPtotS=CUSCPtotS+(CUSCPtot[tech])
  CUSACFS=CUSACFS+(CUSCIF[tech])
  CUSAvCstS=CUSAvCstS+(CUSACF[tech])

CUSPPS=PaybackPeriod(CUSACFS,CUSAvCstS)
CUSEcEfS=EcoEfficiency(CUSACFS,CUSAvCstS,CUSCPtotS)
CUSMACS=MarginalAbatementCost(CUSACFS,CUSCPtotS)


#??Scenario 3(Mixed/Optimal Scenario)

#Definitions
OPTPP=dict()
OPTEcEf=dict()
OPTMAC=dict()
OPTCI=dict()
OPTAC=dict()
OPTCP=dict()
OPTCPtotS=0
OPTACFS=0
OPTAvCstS=0

for tech in CUSPP:
  if CUSPP[tech]<12:
    OPTPP[tech]=CUSPP[tech]
    OPTEcEf[tech]=CUSEcEf[tech]
    OPTMAC[tech]=CUSMAC[tech]
    OPTCI[tech]=CUSCIF[tech]
    OPTAC[tech]=CUSACF[tech]
    OPTCP[tech]=CUSCPtot[tech]

for tech in ECSPP:
  if ECSPP[tech]<12:
    OPTPP[tech]=ECSPP[tech]
    OPTEcEf[tech]=ECSEcEf[tech]
    OPTMAC[tech]=ECSMAC[tech]
    OPTCI[tech]=ECSTotI2017[tech]*ECSAC[tech]
    OPTAC[tech]=ECSAvCsttot[tech]*ECSAC[tech]
    OPTCP[tech]=ECSCPtot[tech]*ECSAC[tech]

for tch in OPTPP:
  OPTCPtotS=OPTCPtotS+(OPTCP[tch])
  OPTACFS=OPTACFS+(OPTCI[tch])
  OPTAvCstS=OPTAvCstS+(OPTAC[tch])

OPTPPS=PaybackPeriod(OPTACFS,OPTAvCstS)
OPTEcEfS=EcoEfficiency(OPTACFS,OPTAvCstS,OPTCPtotS)
OPTMACS=MarginalAbatementCost(OPTACFS,OPTCPtotS)