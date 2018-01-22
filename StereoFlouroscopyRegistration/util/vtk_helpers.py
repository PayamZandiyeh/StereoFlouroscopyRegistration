# -*- coding: utf-8 -*-
'''General utility functions for working with VTK in Python'''

import vtk
import numpy as np

def create_vtkMatrix4x4(orientation):
    '''Create a vtkMatrix4x4 from a numpy array.

    Args:
      orientation (np.array):   The direction matrix

    Returns:
      vtk.vtkMatrix4x4:         The orientation matrix as a vtk object
    '''
    shape = orientation.shape
    assert shape == (4, 4), 'Input orientation must be of shape (4,4) not {}'.format(shape)

    matrix = vtk.vtkMatrix4x4()
    for ii in range(shape[0]):
        for jj in range(shape[1]):
            matrix.SetElement(ii, jj, orientation[ii][jj])
    return matrix
