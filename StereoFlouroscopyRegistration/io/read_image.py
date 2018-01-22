# -*- coding: utf-8 -*-
'''Read a medical image'''

import vtk
import itk
import numpy as np

def get_vtk_reader_from_file_name(file_name):
    '''Find a valid vtkImageReader2 for a give file.

    If no reader can be found, None is returned. Currently, this
    function does not support reading in a DICOM series.

    The following readers are registered beyond the standard:
    vtkNIFTIImageReader, vtkDICOMImageReader.

    Args:
        file_name (string):     Image dimensions

    Returns:
        vtk.vtkImageReader2:    The vtkImageReader2
    '''

    # Add readers which are not registered by default
    vtk.vtkImageReader2Factory.RegisterReader(vtk.vtkNIFTIImageReader())
    # vtk.vtkImageReader2Factory.RegisterReader(vtk.vtkDICOMImageReader())

    # Use factory to return the correct reader
    reader = vtk.vtkImageReader2Factory.CreateImageReader2(file_name)
    return reader
