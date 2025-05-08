import numpy as np
import pandas as pd

def indices(a, func):
    #This is like find in Matlab
    return [i for (i, val) in enumerate(a) if func(val)]

def intersect(a, b):
    return list(set(a) & set(b))

def isempty(x):
    """Checks if a variable is empty."""
    if isinstance(x, (list, tuple, str)):
        return len(x) == 0
    elif isinstance(x, (np.ndarray, pd.Series, pd.DataFrame)):
        return x.size == 0
    else:
        return False

def removenan(Data):
    CData       =   Data.copy()
    NotNanInds  =   indices(CData, lambda x: not np.isnan(x))#find not nan positions
    NotNanVals  =   CData[NotNanInds]
    return NotNanVals,NotNanInds

def rem(a,b):
    return a%b

def ecdf(x):
    xs = np.sort(x)
    ys = np.arange(1, len(xs)+1)/float(len(xs))
    return ys

def pairwise(a,b):
    Data        =   [a,b]
    Data        =   np.sum(Data,axis=0)
    goodlist    =   indices(Data, lambda x: not np.isnan(x))#find not nan positions
    if len(a.shape) == 1:
        a =   a[goodlist]
    elif len(a.shape)==2:
        a = a[:,goodlist]
        
    if len(b.shape) == 1:
        b =   b[goodlist]
    elif len(b.shape)==2:
        b = b[:,goodlist]
    return a,b,goodlist