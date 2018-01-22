# -*- coding: utf-8 -*-
'''General utility functions for working with ITK in Python'''

import itk
import numpy as np

def create_itk_image(dimension, pixel_string, image_region):
    '''Create an ITK image.

    No checks are performed to guarantee the inputs are valid
    inputs.

    Args:
        dimension (int):                Image dimensions
        pixel_string (string):          The pixel type as a string
        image_region (itk.ImageRegion): The image region over which the image is defined

    Returns:
        itk.Image:                      The created ITK image
    '''
    pixel_type = itk.ctype(pixel_string)
    image_type = itk.Image[pixel_type, dimension]
    image = image_type.New()
    image.SetRegions(image_region)
    image.Allocate()

    return image

def create_itk_image_region(dimension, index, size):
    '''Create an ITK image region.

    Image index and size are ordered (x,y,z). The index
    and size should have dimension number of elements. No
    error checking is performed.

    Args:
        dimension (int):  Image dimensions
        index (list):     The starting index of the image
        size (list):      The size of the image

    Returns:
        itk.ImageRegion:  The created ITK image region
    '''
    # Test inputs
    assert len(index) == dimension, "index must be of length dimension"
    assert len(size) == dimension, "size must be of length dimension"

    # Create region
    itk_index = itk.Index[dimension]()
    for idx in range(dimension):
        itk_index[idx] = index[idx]

    itk_size = itk.Size[dimension]()
    for idx in range(dimension):
        itk_size[idx] = size[idx]

    region = itk.ImageRegion[dimension]()
    region.SetSize(itk_size)
    region.SetIndex(itk_index)

    region.SetIndex(itk_index)

    return region

def set_itk_image_origin(image, origin):
    '''Set the origin of an ITK image.

    Origin is ordered (x,y,z). The input image is modified.
    The origin should have the same length as the image has
    dimensions.

    Args:
        image (itk.Image):  Input itkImage
        origin (list):      The starting index of the image

    Returns:
        None
    '''
    assert len(origin) == image.GetImageDimension(), \
      'Origin must be the same size as the image origins'
    np_origin = np.array(origin)
    image.SetOrigin(np_origin)

def set_itk_image_direction(image, direction):
    '''Set the direction matrix of an ITK image.

    Direction matrix should be indexed [row][column]. The input image is
    modified. The direction matrix should have the same number of rows
    and columns as the image has dimensions.

    Args:
        image (itk.Image):  Input itkImage
        direction (np.array):  The direction matrix

    Returns:
        None
    '''
    # Test inputs
    dimension = image.GetImageDimension()
    assert direction.shape == (dimension, dimension), \
        'Direction matrix should have same rows and columns has image has dimensions'

    # Assign the direction matrix
    direction_as_vnl_matrix = image.GetDirection().GetVnlMatrix()
    for ii in range(dimension):
        for jj in range(dimension):
            direction_as_vnl_matrix.put(ii, jj, direction[ii][jj])
