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

def GetRGBColor(color_name):
    '''Return the red, green and blue components for a color as doubles.

    Example taken from vtk example closedSplines.py. According to the documentation
    of vtkNamedColors, the following formats are supported:
        - #RGB (3-digit hexadecimal number, where #4F2 is a shortcut for #44FF22)
        - #RRGGBB (6-digit hexadecimal number)
        - rgb(r, g, b) (where r, g, b are in 0..255 or percentage values)
        - rgba(r, g, b, a) (where r, g, b, are in 0..255 or percentage values, a is in 0.0..1.0)
        - a CSS3 color name (e.g. "steelblue")

    Args:
        colorName (str):  The color name as a string
    Returns:
        tuple:            The tuple of RGB
    '''
    rgb = [0.0, 0.0, 0.0]  # black
    vtk.vtkNamedColors().GetColorRGB(color_name, rgb)
    return rgb

def GetRGBAColor(color_name):
    '''Return the red, green, blue, alpha components for a color as doubles.

    Example taken from vtk example TestPlatonicSolids.py. According to the documentation
    of vtkNamedColors, the following formats are supported:
        - #RGB (3-digit hexadecimal number, where #4F2 is a shortcut for #44FF22)
        - #RRGGBB (6-digit hexadecimal number)
        - rgb(r, g, b) (where r, g, b are in 0..255 or percentage values)
        - rgba(r, g, b, a) (where r, g, b, are in 0..255 or percentage values, a is in 0.0..1.0)
        - a CSS3 color name (e.g. "steelblue")

    Args:
        colorName (str):  The color name as a string
    Returns:
        tuple:            The tuple of RGBA
    '''
    rgba = [0.0, 0.0, 0.0, 1.0] # black
    vtk.vtkNamedColors().GetColor(color_name, rgba)
    return rgba
