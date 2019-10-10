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

    assert hemisphere in ['L', 'R']

    hemi_map = {'L': 'CortexLeft',
                'R': 'CortexRight'}
    hemisphere = hemi_map[hemisphere]

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

def save_surf(vertices, triangles, output, hemisphere=None):

    """
    Save a list of vertices and triangles to a surface file.

    Parameters:
    - - - - -
    vertices: array, float
        3d coordinates of mesh points
    triangles: array, int
        list of mesh triangles
    output: string
        output file name
    hemisphere: string
        'CortexLeft' or 'CortexRight'
    """

    # Initialize meta-data dictionary structure
    meta_dict = {'AnatomicalStructurePrimary': hemisphere,
                 'AnatomicalStructureSecondary': 'GrayWhite',
                 'Caret-Version': '5.65',
                 'GeometricType': 'Anatomical'}

    # Write meta data to GiftiMetaData object
    meta = nb.gifti.gifti.GiftiMetaData()
    for k, v in meta_dict.items():
        nvp = nb.gifti.gifti.GiftiNVPairs(name=k, value=v)
        meta.data.append(nvp)

    # Initialize GiftiCoordSystem object
    coordsys = nb.gifti.gifti.GiftiCoordSystem(dataspace='NIFTI_XFORM_TALAIRACH',
                                               xformspace='NIFTI_XFORM_TALAIRACH',
                                               xform=np.eye(4))

    # Initialize data array of vertices
    d0 = nb.gifti.gifti.GiftiDataArray(intent='NIFTI_INTENT_POINTSET',
                                       datatype='NIFTI_TYPE_FLOAT32',
                                       coordsys=coordsys,
                                       data=vertices,
                                       encoding='GZipBase64Binary',
                                       meta=meta)

    # Initialize data array of triangles
    d1 = nb.gifti.gifti.GiftiDataArray(intent='NIFTI_INTENT_TRIANGLE',
                                    datatype='NIFTI_TYPE_INT32',
                                    coordsys=coordsys,
                                    data=triangles,
                                    encoding='GZipBase64Binary')

    S = nb.gifti.gifti.GiftiImage(darrays=[d0,d1])
    S.to_filename(output)
