# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 10:43:58 2017

@author: kristianeschenburg
"""

import numpy as np
import nibabel as nb
import scipy.io as sio

import os
import csv,h5py,pickle

def load(datafile,**kwargs):

        assert os.path.exists(datafile)
        filename, file_extension = os.path.splitext(datafile)

        function_map = {'.mat': loadMat,
                        '.gii': loadGii,
                        '.h5': loadH5,
                        '.p': loadPick,
                        '.csv': loadCSV}

        return function_map[file_extension](datafile,**kwargs)
        

def loadMat(infile,datasets=None,group=None):
    
    """
    Method to load .mat files.
    
    Parameters:
    - - - - -
        matFile : input .mat file
        datasets : if you want a specific key array, supply name of key
    """

    try:
        matData = h5py.File(infile,mode='r')
    except:
        try:
            matData = sio.loadmat(infile)
        except:
            err = 'Cannot read with h5py or scipy.io.'
            raise IOError(err)

    if datasets:
        try:
            mat = np.asarray(matData[datasets]).squeeze()
        except:
            pass
        else:
            if type(matData) == h5py._hl.files.File:
                mat = mat.T

    else:
        for k in matData.keys():
            if k.startswith('_'):
                del matData[k]  
        key = matData.keys()[0]
        mat = np.asarray(matData[key]).squeeze()
        
        if type(matData) == h5py._hl.files.File:
                mat = mat.T

    if type(matData) == h5py._hl.files.File:
        matData.close()

    return mat


def loadGii(infile,datasets=[],group=None):
    
    """
    Method to load Gifti files.
    
    Parameters:
    - - - - -
        giiFile : input gifti (or .nii) file
        darrayID : if array is .gii, often comes with multiple arrays -- you can
                    choose to specify which one
    """

    try:
        gii = nb.load(infile)
    except:
        raise IOError('{} cannot be read.'.format(infile))
    
    if isinstance(datasets,int):
        datasets = [datasets]
    elif isinstance(datasets,np.ndarray):
        datasets = list(datasets)
    elif datasets==[]:
        datasets = list(np.arange(len(gii.darrays)))

    if isinstance(gii,nb.gifti.GiftiImage):
        darray = []
        for j in datasets:
            darray.append(np.asarray(gii.darrays[j].data).squeeze())
        darray = np.column_stack(darray).squeeze()
    elif isinstance(gii,nb.nifti2.Nifti2Image):
        darray = np.asarray(gii.get_data()).squeeze()
    else:
        raise IOError('Cannot access array data.')
    
    return darray
    

def loadH5(infile,datasets=None,group=None):
    
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
    
    assert os.path.exists(infile)
    
    try:
        h5 = h5py.File(infile,'r')
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
    

def loadPick(infile,datasets=None,group=None):
    
    """
    Method to load pickle file.  Not part of a specific class.
    
    Parameters:
    - - - - -
        pickleFile : input pickle file
    """
    
    assert os.path.exists(infile)

    try:
        with open(infile,"rb") as inPickle:
            pick = pickle.load(inPickle)
    except:
        raise IOError('File cannot be loaded.')
    
    return pick


def loadCSV(infile,datasets=None,group=None):
    
    """
    Method to read csv file.
    
    Parameters:
    - - - - -
        inCSV : input csv file
    """
    
    assert os.path.exists(infile)
    
    csv_data = []
    with open(infile,'rb') as inCSV:
        readCSV = csv.reader(inCSV,delimiter=',')
        for row in readCSV:
            R = map(float,row)
            csv_data.append(np.asarray(R).squeeze())
        
    csv_data = np.asarray(csv_data).squeeze()
    
    return csv_data
