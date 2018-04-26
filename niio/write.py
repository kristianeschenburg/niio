#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:23:17 2017

@author: kristianeschenburg
"""

import nibabel as nb
import numpy as np

def writeGiftiImage(dataVector,outputName,hemisphere=None):
    
    """
    
    Vector needs to have the same number of indices as the surface
    it will be overlaid on.
    
    Save outputName with BASENAME.func.gii extension.  .func specifies
    a float metric file.
    
    Parameters:
    - - - - -
        dataVector : list of vectors to save as Gifti file
        outputName : output file name
        hemisphere : 'CortexLeft' or 'CortexRight', depending on hemisphere
        
        
    To visualize, install Connectome Workbench and enter following command:
        
        wb_view outputName ${surfaceFile}.surf.gii
    
    The hemisphere of the surface must match hemisphere parameter.
    
    """
    
    assert hemisphere in ['CortexLeft','CortexRight']

    # Create name-value meta data pairs (used for loading in image viewer)
    nvPair = nb.gifti.GiftiNVPairs(name='AnatomicalStructurePrimary',
                                   value=hemisphere)
    metaData = nb.gifti.GiftiMetaData(nvPair)
    
    # Generate GiftiImage object containing data vector and meta data
    gi = nb.gifti.GiftiImage(meta = metaData)
    
    if isinstance(dataVector,list):
        for dv in dataVector:

            newVector = np.asarray(dv).squeeze().astype(np.float32)
            gda = nb.gifti.GiftiDataArray(data=newVector)
            gi.add_gifti_data_array(gda)
    
    else:
        newVector = np.asarray(dataVector).squeeze().astype(np.float32)
        gda = nb.gifti.GiftiDataArray(data=newVector)
        gi.add_gifti_data_array(gda)

    nb.save(gi,outputName)
    
    
def giftiColorMap(colormap):
    
    with open(colormap,'r') as cmap:
        c = cmap.readlines()

    labelTable = nb.gifti.GiftiLabelTable()
    
    for l in np.arange(0,len(c),2):
        lm = labelMap(c[l],c[l+1])
        labelTable.labels.append(lm)

    return labelTable


def labelMap(name,vrgba):
    
    """
    Generate a mapping of label value to name, red, blue, green, alpha.
    """
    
    name = name.strip()
    colors = vrgba.strip().split(' ')
    colors = map(int,colors)
    
    label = nb.gifti.GiftiLabel(key=colors[0],
                                red=colors[1],
                                green=colors[2],
                                blue=colors[3],
                                alpha=colors[4])
    label.label = name
    
    return label
