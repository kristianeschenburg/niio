# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 10:43:58 2017

@author: kristianeschenburg
"""

import numpy as np
import nibabel

import os
import csv,h5py,pickle
import scipy.io as sio


def loadMat(matFile,*dataset):
    
    """
    Method to load .mat files.
    
    Parameters:
    - - - - -
        matFile : input .mat file
        datasets : if you want a specific key array, supply name of key
    """
    
    assert os.path.exists(matFile)

    try:
        matData = sio.loadmat(matFile)
    except:
        raise NotImplementedError('Cannot load matrix file with scipy.io.')
    else:
        if dataset:
            try:
                mat = matData[dataset]
            except:
                raise KeyError('File not have key {}'.format(dataset))
            else:
                mat = np.asarray(matData[dataset]).squeeze()
        else:
            for k in matData.keys():
                if k.startswith('_'):
                    del matData[k]     
            mat = np.asarray(matData[matData.keys()[0]]).squeeze()
        
    return mat

def loadGii(giiFile,darrayID=0):
    
    """
    Method to load Gifti files.
    
    Parameters:
    - - - - -
        giiFile : input gifti (or .nii) file
        darrayID : if array is .gii, often comes with multiple arrays -- you can
                    choose to specify which one
    """
    
    assert os.path.exists(giiFile)
    
    if isinstance(darrayID,int):
        darrayID = [darrayID]
    else:
        darrayID = list(darrayID)
    
    try:
        gii = nibabel.load(giiFile)
    except:
        raise IOError('{} cannot be read.'.format(giiFile))

    if isinstance(gii,nibabel.gifti.GiftiImage):
        darray = []
        for j in darrayID:
            darray.append(np.asarray(gii.darrays[j].data).squeeze())
        darray = np.column_stack(darray).squeeze()
    elif isinstance(gii,nibabel.nifti2.Nifti2Image):
        darray = np.asarray(gii.get_data()).squeeze()
    else:
        raise IOError('Cannot access array data.')
    
    return darray
    
def loadH5(inFile,datasets=None,group=None):
    
    """
    Method to load hdf5 files.
    
    Parameters:
    - - - - -
        inFile : input file name
        datasets : attributes in file to be extracted.  If not specified, returns
                dictionary of all key-value pairs in file.
        group : group in which datasets are contained.  If not group, datasets
                assumed to exist at top level of file structure.
    """
    
    assert os.path.exists(inFile)
    
    try:
        h5 = h5py.File(inFile,'r')
    except:
        raise IOError('File cannot be loaded.')

    # If user specifies an object group containing data
    data = {}    
    if group:
        try:
            h5Lower = h5[group]
            h5.close()
        except:
            raise KeyError('File does not have group {}.'.format(group))
    else:
        h5Lower = h5
        
    # If User specifies specific object datasets
    if not datasets:
        datasets = h5Lower.keys()
        
    for k in datasets:
        try:
            data[k] = np.asarray(h5Lower[k])
        except:
            raise KeyError('File does not have attribute {}.'.format(k))
    
    h5Lower.close()
    
    return data
    

def loadPick(pickleFile):
    
    """
    Method to load pickle file.  Not part of a specific class.
    
    Parameters:
    - - - - -
        pickleFile : input pickle file
    """
    
    assert os.path.exists(pickleFile)

    try:
        with open(pickleFile,"rb") as inPickle:
            pick = pickle.load(inPickle)
    except:
        raise IOError('File cannot be loaded.')
    
    return pick


def loadCSV(csvFile):
    
    """
    Method to read csv file.
    
    Parameters:
    - - - - -
        inCSV : input csv file
    """
    
    assert os.path.exists(csvFile)
    
    csv_data = []
    with open(csvFile,'rb') as inCSV:
        readCSV = csv.reader(inCSV,delimiter=',')
        for row in readCSV:
            R = map(float,row)
            csv_data.append(np.asarray(R).squeeze())
        
    csv_data = np.asarray(csv_data).squeeze()
    
    return csv_data
