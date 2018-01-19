# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 10:43:58 2017

@author: kristianeschenburg
"""

import numpy as np
import nibabel

import h5py
import os
import pickle
import scipy.io as sio


def loadMat(inFile,*dataset):
    
    """
    Method to load .mat files.  Not part of a specific class.
    """
    
    assert os.path.exists(inFile)

    try:
        matData = sio.loadmat(inFile)
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

def loadGii(inFile,darray=0,*args):
    
    """
    Method to load Gifti files.  Not part of a specific class.
    """
    
    parts = str.split(inFile,'/')
    if isinstance(darray,int):
        darray = [darray]
    else:
        darray = list(darray)
    
    try:
        data = nibabel.load(inFile)
    except OSError:
        print('Warning: {} cannot be read.'.format(parts[-1]))
    else:
        # if data is instance of GiftiImage
        if isinstance(data,nibabel.gifti.gifti.GiftiImage):
            label = []
            for j in darray:
                label.append(np.squeeze(data.darrays[j].data))
            label = np.column_stack(label).squeeze()
            
        # if data is instance of Nifti2Image
        elif isinstance(data,nibabel.nifti2.Nifti2Image):
            label = np.squeeze(np.asarray(data.get_data()))
        elif isinstance(data,nibabel.cifti2.cifti2.Cifti2Image):
            label = np.squeeze(np.asarray(data.get_data()));
        
        return label
        
    
def loadH5(inFile,datasets=None,group=None):
    
    """
    Method to load hdf5 files.  Not part of specific class.
    
    Parameters:
    - - - - -
        inFile : input file name
        group : group in which datasets are contained.  If not group, datasets
                assumed to exist at top level of file structure.
        datasets : attributes in file to be extracted.  If not specified, returns
                dictionary of all key-value pairs in file.
    """
    
    assert os.path.exists(inFile)
    
    try:
        h5 = h5py.File(inFile,'r')
    except:
        raise IOError('File cannot be loaded.')

    data = {}    
    if group:
        try:
            h5Lower = h5[group]
            h5.close()
        except:
            raise KeyError('File does not have group {}.'.format(group))
    else:
        h5Lower = h5
        
    if not datasets:
        datasets = h5Lower.keys()
        
    for k in datasets:
        try:
            data[k] = np.asarray(h5Lower[k])
        except:
            raise KeyError('File does not have attribute {}.'.format(k))
    
    h5Lower.close()
    
    return data
    

def loadPick(inFile,*args):
    
    """
    Method to load pickle file.  Not part of a specific class.
    """

    parts = str.split(inFile,'/')

    try:
        with open(inFile,"rb") as toRead:
            data = pickle.load(toRead)
    except OSError:
        print('Warning: {} cannot be read.'.format(parts[-1]))
    else:
        return data


"""
def parseH5(h5Object,featureNames):
    

    # We are loading the H5 objects as read only.  parseH5 copy the contents of
    # the h5 object to a dictionary.

    groups = h5Object.keys()
    parsedData = {str(s): {}.fromkeys(featureNames) for s in groups}
    'Parsing {} for all subjects.'.format(featureNames)
 
    for s in groups:

        cond = True
        for f in featureNames:
            if f in h5Object[s].keys():
                parsedData[str(s)][f] = np.asarray(h5Object[str(s)][f])
            else:
                cond = False
        if not cond:
            del parsedData[s]
    
    return parsedData
"""