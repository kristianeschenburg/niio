#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:23:17 2017

@author: kristianeschenburg
"""

import nibabel as nb
import numpy as np


def save(func, output, hemisphere=None):
    """
    Save a vector as a *.func.gii file.

    Parameters:
    - - - - -
    dataVector : list of vectors to save as Gifti file
    output : output file name
    hemisphere : 'CortexLeft' or 'CortexRight', depending on hemisphere

    Example:
    - - - -
    Save Default Mode Network ICA component to file.

    >>> save(ica_dmn,'DefaultMode.func.gii','CortexLeft')

    """

    assert hemisphere in ['CortexLeft', 'CortexRight']

    # Create name-value meta data pairs (used for loading in image viewer)
    nvPair = nb.gifti.GiftiNVPairs(name='AnatomicalStructurePrimary',
                                        value=hemisphere)
    metaData = nb.gifti.GiftiMetaData(nvPair)

    # Generate GiftiImage object containing data vector and meta data
    gifti_image = nb.gifti.GiftiImage(meta=metaData)

    if isinstance(func, list):
        for dv in func:

            newVector = np.asarray(dv).squeeze().astype(np.float32)
            gda = nb.gifti.GiftiDataArray(data=newVector)
            gifti_image.add_gifti_data_array(gda)

    else:
        newVector = np.asarray(func).squeeze().astype(np.float32)
        gda = nb.gifti.GiftiDataArray(data=newVector)
        gifti_image.add_gifti_data_array(gda)

    nb.save(gifti_image, output)
