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


def midline(vector):
    
    """
    Method to compute the midline coordinates of a label set.
    
    Not yet tested on the output of FreeSurfer for a new IBIC subject.
        
    Assumes midline vertices will have label of 0 or -1.  Could be changed to
    accept specific value.
    
    """

    coords = np.squeeze(np.where(vector == 0))
    
    return coords

def midline_restingState(inRest,outFile,times):
    
    """
    
    Method to compute the midline coordinates from a resting state file.
    This is generally what we will use to pre-compute the midline indices for
    each brain, since it doesn't make sense to compute a cortical ROI for a
    a region that does not have BOLD activity.
    
    Paramters:
    - - - - - 
        
        inRest : path to resting state file
        
        outFile : name of output midline indices file
    
    """
    
    restParts = inRest.split('.')
    
    if restParts[-1] == 'mat':
        print '.mat file'
        try:
            rest = loadMat(inRest)
        except:
            return
    elif restParts[-1] == 'gii':
        print '.gii file'
        try:
            rest = loadGii(inRest,np.arange(times))
        except:
            return
    else:
        raise('Resting state is neither a gifti or .mat file.')
        
    print 'Resting state shape: {}'.format(rest.shape)

    temp = np.sum(np.abs(rest),axis=1)
    
    # We add one so we can also use these files in matlab -- when loading back
    # into python, we must take care to subtract 1 again
    mids = np.squeeze(np.where(temp == 0)) + 1
    
    m = {}
    m['mids'] = mids
        
    sio.savemat(outFile,m)
    

def fixMatching(matching,sN,sMids,tN,tMids):
    
    """
        
    Method to adjust the coordinates and shape of a match.
    
    For example, with the HCP data, the original data is 32492 vertices.  We
    excluded the 2796 midline vertices in the surface matching step (so we 
    included only 29696 total vertices).  The indices in the match correspond
    to positions between 1 and 29696, not 1 and 32492.
    
    This method corrects for the coordiante differences, and returns a 
    matching of length sN.
    
    Expects that the matching has already been adjusted for the
    Matlab-to-Python indexing conversion (i.e. that 1 has been subtracted).
    
    The current method works for matching between surfaces with different
    numbers of surface vertices and different midline coordinates.
    
    Paramters:
    - - - - - 
        matching : output of DiffeoSpectralMatching (corr12, corr21)    
        sN : number of vertices in full source surface    
        sMids : vector containing indices of midline for source surface    
        tN : number of vertices in full target surface    
        tMids : vector containing indices of midline for target surface
                
    Returns:
    - - - - 
        adjusted : list where matching indices are converted to range of
                    surface vertices
    """
    
    # get coordinates of vertices in target surface not in the midline
    full_coords = list(set(np.arange(tN)).difference(set(tMids)))
    
    # get list of coordinates of length matching
    match_coords = list(np.arange(len(matching)))

    # create dictionary mapping matching numbers to non-midline coords
    convert = dict((m,f) for m,f in zip(match_coords,full_coords))
    
    # convert the matching coordinates to non-midline coordinates
    adjusted = list(convert[x] for x in list(matching))
    
    if len(adjusted) < sN:
    
        cdata = np.zeros(shape=(sN,1))
        coords =list(set(np.arange(sN)).difference(set(sMids)))
        cdata[coords,0] = adjusted
        cdata[list(sMids),0] = -1
             
        adjusted = cdata
    
    return np.squeeze(adjusted)


def fixLabelSize(mids,dL,N):
    
    """
    Given a surface file of proper size (like the FreeSurfer Myelin Map) and
    label file that excludes the midline, adjust the size of the defunct
    label file to match that of the proper file.
    """

    coords = list(set(np.arange(N)).difference(set(mids)))
    
    cdata = np.zeros(shape=(N,1))
    cdata[coords,0] = dL
    
    return np.squeeze(cdata)


def loadMat(inFile,*args):
    
    """
    Method to load .mat files.  Not part of a specific class.
    """

    if os.path.isfile(inFile):
        try:
            data = sio.loadmat(inFile)
        except NotImplementedError:
            data = h5py.File(inFile)
            data = np.transpose(np.asarray(data[data.keys()[0]]))
        else:    
            for k in data.keys():
                if k.startswith('_'):
                    del data[k]       
            data = np.squeeze(np.asarray(data.get(data.keys()[0])))   
            
        return data
    
    else:
        print('Input file does not exist.')

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
        
def loadH5(inFile,*keys):
    
    """
    Method to load hdf5 files.  Not part of specific class.
    
    Parameters:
    - - - - -
        inFile : input file name
        keys : attributes contained in hdf5 file to be extracted
                If len(keys) == 1, returns a Numpy array.  Otherwise, returns a dictionary,
                where keys as elements of keys parameter, and values as attributes in inFile.
    """

    parts = str.split(inFile,'/')

    try:
        toRead = h5py.File(inFile,'r')
    except IOError:
        raise
    else:
        if not keys:
            key = toRead.keys()[0]
            data = np.asarray(toRead[key])
        elif 'full' in keys:
            data = toRead
        else:
            data = {}
            for k in keys:
                if k in toRead.keys():
                    data[k] = np.asarray(toRead[k])
                else:
                    raise KeyError('{} not in {}.'.format(k,parts[-1]))
    
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


def parseH5(h5Object,featureNames):
    
    """
    We are loading the H5 objects as read only.  parseH5 copy the contents of
    the h5 object to a dictionary.
    """
    
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


def loadH5_dbscan(inFile):
    
    """
    Method to load results of dbscan sample reduction.
    """
    
    inData = h5py.File(inFile,mode='r')
    labels = [np.int32(x) for x in inData['maps'].keys()]
    dbscan_data = {}.fromkeys(labels)
    
    for feat in labels:
        dbscan_data[feat] = np.asarray(inData['dbscan_data'][str(feat)])
        
    inData.close()
    
    return dbscan_data
    
    
def saveH5_dbscan(outFile,inDict):
    
    """
    Method to save results of dbscan sample reduction.
    """
    
    outFile = h5py.File(outFile,'w')
    labels = inDict.keys()
    
    outFile.create_group('maps')
    outFile.create_group('dbscan_data')
    
    for lab in labels:
        outFile['maps'].create_dataset(str(lab),data=lab)
        outFile['dbscan_data'].create_dataset(str(lab),data=inDict[lab])
    
    outFile.close()
    
                
