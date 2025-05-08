import UtilityFunctions as ut
import numpy  as np
from   scipy import stats
#import pandas as pd
#from   pandas.stats.api import ols
#from   openpyxl import load_workbook
#from   dotmap import DotMap
#pandas.qcut(x, q, labels=None, retbins=False, precision=3)[source]
#if (__name__ == "__main__"):  # Execute when invoked from command line


def CleanData(Data,N):
#Cleans an array by asset and period by removing outliers
    [NumAsset,NumPeriod] = Data.shape
    CD          =   Data.copy() #Copied
    grandmedian =   np.nanmedian(CD)
    Qset        =   [25,75] #inner quartile range
    Qbreaks     =   np.nanpercentile(np.ravel(CD), Qset, axis = 0)
    QHQL        =   Qbreaks[1]-Qbreaks[0]
    for a in range(0,NumAsset):
        for p in range(0,NumPeriod):
             x = CD[a,p]
             if not np.isnan(x):           
                if x >= grandmedian:
                    xc = min(x,grandmedian+(N*QHQL));
                if x < grandmedian:
                    xc = max(x,grandmedian-(N*QHQL));
                CD[a,p] = xc;
    return CD

def ctn(Data,UnitNormal):  
#UnitNormal 1 for unit normal, 0 retain original mean and variance
#Convert data to a normal distribution
    TD                          =   Data.copy()
    [NotNaNvalues,NotNaninds]   =   ut.removenan(TD)
    if UnitNormal == 0:
        nanmean = np.nanmean(TD)
        nanstd  = np.nanstd(TD)
    if not ut.isempty(NotNaninds):
        NumNotNan           =   len(NotNaninds)
        empericalcdf        =   ut.ecdf(NotNaNvalues)
        NormalData          =   NotNaNvalues*np.nan
        SortedDatainds      =   np.argsort(NotNaNvalues) #Index to sorted data positions
        for j in range(0,NumNotNan):    #%Interpolate to interval [MinCS,MaxCS]
            #inverse cumulative distribution or quantile function 
            #is STUDIDLY named ppf (percent point function)        
            if UnitNormal == 1:          
                icdf            = stats.norm.ppf(empericalcdf[j])
                if np.isinf(icdf):
                    MaxCS       = empericalcdf[j-1] + (empericalcdf[j] - empericalcdf[j-1])/2
                    icdf        = stats.norm.ppf(MaxCS)
            elif UnitNormal == 0:
                icdf            = stats.norm.ppf(empericalcdf[j], loc = nanmean, scale = nanstd)
                if np.isinf(icdf):
                    MaxCS       = empericalcdf[j-1] + (empericalcdf[j] - empericalcdf[j-1])/2
                    icdf        = stats.norm.ppf(MaxCS, loc = nanmean, scale = nanstd)
            NormalData[j] =   icdf #inverse cumulative distribution of norman density
            TD[NotNaninds[SortedDatainds[j]]]  = NormalData[j]
            
    return  TD


def ZSBT(Data,D):
    TD          = np.nan*np.zeros([Data.shape[0],Data.shape[1]])
    print('z-score by time')
    for a in range(0,D['NumAsset']):
        DataZ       = Data[a,:]   #Row at time a
        NumNotNan   = len(DataZ) - np.sum(np.isnan(DataZ))
        if not ut.isempty(DataZ) and NumNotNan >= 5:
            DataZ   = (DataZ-np.nanmean(DataZ))/np.nanstd(DataZ)
            TD[a,:] = DataZ       
    return TD

def ZSCS(Data,D):
    TD          = np.nan*np.zeros([Data.shape[0],Data.shape[1]])
    print('z-score by crosssection')
    for p in range(0,D['NumPeriod']):
        DataZ   = Data[:,p]#Column at time p
        NumNotNan = len(DataZ) - np.sum(np.isnan(DataZ))
        if NumNotNan >=5:
            DataZ   = (DataZ-np.nanmean(DataZ))/np.nanstd(DataZ)
            TD[:,p] = DataZ
    return TD

def ZSCSBS(Data,D):
    TD          = np.nan*np.zeros([Data.shape[0],Data.shape[1]])
    print('z-score by crosssection by sector')
    for p in range(0,D['NumPeriod']):
        for s in range(0,D['NumSector']):
            csectorcode = D['SectorCode'][s]
            inds  = ut.indices(D['Sector_Asset'], lambda x: x == csectorcode) #like find in Matlab            )
            if not ut.isempty(inds) : #Check for empty list
                DataZ       = Data[inds,p]
                NumNotNan   = len(DataZ) - np.sum(np.isnan(DataZ))
                if NumNotNan >=5:
                    DataZ       = (DataZ-np.nanmean(DataZ))/np.nanstd(DataZ)
                    TD[inds,p]  =  DataZ
    return TD

def ZSCSBI(Data,D):
    TD          = np.nan*np.zeros([Data.shape[0],Data.shape[1]])
    print('z-score by crosssection by industry')
    for p in range(0,D['NumPeriod']):
        for i in range(0,D['NumIndustry']):
            cindustrycode   =   D['IndustryCode'][i]
            inds            =   ut.indices(D['Industry_Asset'], lambda x: x == cindustrycode) #like find in Matlab
            if not ut.isempty(inds): #Check for empty list
                DataZ       = Data[inds,p]
                NumNotNan   = len(DataZ) - np.sum(np.isnan(DataZ))
                if NumNotNan >=5:
                    DataZ       = (DataZ-np.nanmean(DataZ))/np.nanstd(DataZ)
                    TD[inds,p]  =  DataZ     
    return TD

def FNBT(Data,D):
    UnitNormal  = 0
    TD          = np.nan*np.zeros([Data.shape[0],Data.shape[1]])
    print('fit to normal by time')
    for a in range(0,D['NumAsset']):
        Data1       = Data[a,:] #Row at time a
        NumNotNan   = len(Data1) - np.sum(np.isnan(Data1))
        if NumNotNan >=5:
            NormalData  = ctn(Data1,UnitNormal)
            TD[a,:]     = NormalData
    return TD

def FNCS(Data,D):
    UnitNormal  = 0
    TD          = np.nan*np.zeros([Data.shape[0],Data.shape[1]])
    print('fit to normal by crosssection')
    for p in range(0,D['NumPeriod']):
        DataP       = Data[:,p]#Column at time p
        NumNotNan   = len(DataP) - np.sum(np.isnan(DataP))
        if NumNotNan >=5:
            NormalData  = ctn(DataP,UnitNormal)
            TD[:,p]     = NormalData
    return TD

def FNCSBS(Data,D):
    UnitNormal  = 0
    TD          = np.nan*np.zeros([Data.shape[0],Data.shape[1]])
    print('fit to normal by crosssection by sector')
    for p in range(0,D['NumPeriod']):
        for s in range(0,D['NumSector']):
            csectorcode = D['SectorCode'][s]
            inds        = ut.indices(D['Sector_Asset'], lambda x: x == csectorcode) #like find in Matlab            )
            if not ut.isempty(inds): #Check for empty list
                DataS       = Data[inds,p]
                NumNotNan   = len(DataS) - np.sum(np.isnan(DataS))
                if NumNotNan >=5:
                    NormalData  = ctn(DataS,UnitNormal)
                    TD[inds,p]  =  NormalData
    return TD

def FNCSBI(Data,D):
    UnitNormal  = 0
    TD          = np.nan*np.zeros([Data.shape[0],Data.shape[1]])
    print('fit to normal by crosssection by industry')
    for p in range(0,D['NumPeriod']):
        for i in range(0,D['NumIndustry']):
            cindustrycode   = D['IndustryCode'][i]
            inds            = ut.indices(D['Industry_Asset'], lambda x: x == cindustrycode) #like find in Matlab
            if not ut.isempty(inds): #Check for empty list
                DataI       =  Data[inds,p]
                NumNotNan   = len(DataI) - np.sum(np.isnan(DataI))
                if NumNotNan >=5:
                    NormalData  =  ctn(DataI,UnitNormal)
                    TD[inds,p]  =  NormalData        
    return TD

def QUCS(Data,D,NumTile):
    print('quantile by crosssection, (' + str(NumTile) + ' quantiles' +')')
    Start   =   1.0/NumTile
    Stop    =   ((NumTile-1)*1.0)/NumTile
    Qset    =   np.linspace(Start,Stop, num=NumTile-1)*100
    TD          = np.nan*np.zeros([Data.shape[0],Data.shape[1]])
    #Find the quantile breaks by period 
    Qbreaks =   np.nanpercentile(Data, Qset, axis = 0, keepdims=True)
    Qbreaks =   np.squeeze(Qbreaks, axis=(1,))
    for p in range(0,D['NumPeriod']):
        ColData =   Data[:,p]               #Column at time p
        Qb      =   Qbreaks[:,p]            #quantile breaks at time p
        Qb      =   np.insert(Qb,0,-np.inf) #lowest value
        Qb      =   np.append(Qb,np.inf)    #Highest value
        for q in range(1,NumTile+1):        #q is 1,2,...,NumTile
            lb      = Qb[q-1]
            ub      = Qb[q]
            Quantileinds  = ut.indices(ColData, lambda x: x >= lb and x < ub)
            if not ut.isempty(Quantileinds):
                TD[Quantileinds,p] = q            
    return TD

def QUCSBS(Data,D,NumTile):
    print('quantile by crosssection by sector, (' + str(NumTile) + ' quantiles' +')')
    Start   =   1.0/NumTile
    Stop    =   ((NumTile-1)*1.0)/NumTile
    Qset    =   np.linspace(Start,Stop, num=NumTile-1)*100
    TD      =   np.nan*np.zeros([Data.shape[0],Data.shape[1]])
    for s in range(0,D['NumSector']):
        csectorcode = D['SectorCode'][s]
        Sectorinds  = ut.indices(D['Sector_Asset'], lambda x: x == csectorcode) #like find in Matlab            )
        if not ut.isempty(Sectorinds) : #Check for empty list
            DataS       = Data[Sectorinds,:] #Sector data by time
            DataQS      = Data[Sectorinds,:]*np.nan
            #Find the quantile breaks for this sector by period 
            Qbreaks =   np.nanpercentile(DataS, Qset, axis = 0, keepdims=True)
            Qbreaks =   np.squeeze(Qbreaks, axis=(1,))
            for p in range(0,D['NumPeriod']):
                ColData =   DataS[:,p]              #Column for sector at time p
                Qb      =   Qbreaks[:,p]            #quantile breaks for sector at time p
                Qb      =   np.insert(Qb,0,-np.inf) #lowest value, inserted to make looping easy
                Qb      =   np.append(Qb,np.inf)    #Highest value, inserted to make looping easy
                for q in range(1,NumTile+1):        #q is 1,2,...,NumTile
                    lb              = Qb[q-1]
                    ub              = Qb[q]
                    Quantileinds    = ut.indices(ColData, lambda x: x >= lb and x < ub)
                    if not ut.isempty(Quantileinds):
                        DataQS[Quantileinds,p] = q 
            TD[Sectorinds,:] = DataQS         
    return TD

def QUCSBI(Data,D,NumTile):
    print('quantile by crosssection by industry, (' + str(NumTile) + ' quantiles' +')')
    Start   =   1.0/NumTile
    Stop    =   ((NumTile-1)*1.0)/NumTile
    Qset    =   np.linspace(Start,Stop, num=NumTile-1)*100
    TD      =  np.nan*np.zeros([Data.shape[0],Data.shape[1]])
    for i in range(0,D['NumIndustry']):
        cindustrycode   = D['IndustryCode'][i]
        Industryinds    = ut.indices(D['Industry_Asset'], lambda x: x == cindustrycode) #like find in Matlab            )
        if not ut.isempty(Industryinds) : #Check for empty list
            DataI       = Data[Industryinds,:] #Industry data by time
            DataQI      = Data[Industryinds,:]*np.nan
            #Find the quantile breaks for this industryr by period 
            Qbreaks =   np.nanpercentile(DataI, Qset, axis = 0, keepdims=True)
            Qbreaks =   np.squeeze(Qbreaks, axis=(1,))
            for p in range(0,D['NumPeriod']):
                ColData =   DataI[:,p]              #Column for industry at time p
                Qb      =   Qbreaks[:,p]            #quantile breaks for industry at time p
                Qb      =   np.insert(Qb,0,-np.inf) #lowest value, inserted to make looping easy
                Qb      =   np.append(Qb,np.inf)    #Highest value, inserted to make looping easy
                for q in range(1,NumTile+1):        #q is 1,2,...,NumTile
                    lb              = Qb[q-1]
                    ub              = Qb[q]
                    Quantileinds    = ut.indices(ColData, lambda x: x >= lb and x < ub)
                    if not ut.isempty(Quantileinds):
                        DataQI[Quantileinds,p] = q 
            TD[Industryinds,:] = DataQI         
    return TD

def Transform(Data_AP,TransformList,D):
    TD = Data_AP.copy() #Must work with a copy, not a pointer
    print('Applying transformations ...')
    for transformation in TransformList:
        print(transformation)
        if   transformation == 'ZSBT':
            TD = ZSBT(TD,D)
        elif transformation == 'ZSCS':
            TD = ZSCS(TD,D)
        elif transformation == 'ZSCSBS':
            TD = ZSCSBS(TD,D)
        elif transformation == 'ZSCSBI':
            TD = ZSCSBI(TD,D)
        elif transformation == 'FNBT':
            TD = FNBT(TD,D)    
        elif transformation == 'FNCS':
            TD = FNCS(TD,D)
        elif transformation == 'FNCSBS':
            TD = FNCSBS(TD,D)
        elif transformation == 'FNCSBI':
            TD = FNCSBI(TD,D)
        elif transformation == 'Q2CS':
            NumTile = 2
            TD = QUCS(TD,D,NumTile)
        elif transformation == 'Q3CS':
            NumTile = 3
            TD = QUCS(TD,D,NumTile)           
        elif transformation == 'Q5CS':
            NumTile = 5
            TD = QUCS(TD,D,NumTile)
        elif transformation == 'Q7CS':
            NumTile = 7
            TD = QUCS(TD,D,NumTile) 
        elif transformation == 'Q10CS':
            NumTile = 10
            TD = QUCS(TD,D,NumTile)        
        elif transformation == 'Q2CSBS':
            NumTile = 2
            TD = QUCSBS(TD,D,NumTile)
        elif transformation == 'Q3CSBS':
            NumTile = 3
            TD = QUCSBS(TD,D,NumTile)           
        elif transformation == 'Q5CSBS':
            NumTile = 5
            TD = QUCSBS(TD,D,NumTile) 
        elif transformation == 'Q10CSBS':
            NumTile = 10
            print('at Q10CSBS')
            TD = QUCSBS(TD,D,NumTile) 
            print('after Q10CSBS')
        elif transformation == 'Q2CSBI':
            NumTile = 2
            TD = QUCSBI(TD,D,NumTile)
        elif transformation == 'Q3CSBI':
            NumTile = 3
            TD = QUCSBI(TD,D,NumTile)           
        elif transformation == 'Q5CSBI':
            NumTile = 5
            TD = QUCSBI(TD,D,NumTile)
            
    print('Transformations applied')
    return TD

 