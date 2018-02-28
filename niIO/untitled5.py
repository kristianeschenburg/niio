#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:49:56 2018

@author: kristianeschenburg
"""

import numpy as np
from scipy.spatial.distance import cdist

def maxRegionalCorrelation(sourceInds,targetInds,samples):
    
    """
    For all indices in list of source indices, compute which single
    target index it correlates most strongly with.
    
    Parameters:
    - - - - -
        sourceInds : list of source indices
        targetInds : list of target indices
        samples : V x F feature matrix (V = number of indices in whole map,
                    F = number of features))
    """
    
    sSamples = samples[sourceInds,:]
    tSamples = samples[targetInds,:]
    
    crossCorr = 1-cdist(sSamples,tSamples,metric='correlation')
    
    maxCorrelateIndices = targetInds[np.argmax(crossCorr,axis=1)]
    maxCorrelates = np.max(crossCorr,axis=1)
    
    return [maxCorrelateIndices,maxCorrelates]

def maxRegionalProjection(sourceInds,targetInds,samples):
    
    """
    For all indices in list of source indices, compute which single target 
    index it sends the most streamline projections to.
    
    Parameters:
    - - - - -
        sourceInds : list of source indices
        targetInds : list of target indices
        samples : V x V streamline projection matrix
    """
    
    sData = samples[sourceInds,:][:,targetInds]
    
    maxProjectionIndices = targetInds[np.argmax(sData,axis=1)]
    maxProjections = np.max(sData,axis=1)
    
    return [maxProjectionIndices,maxProjections]