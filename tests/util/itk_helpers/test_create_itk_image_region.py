'''Test StereoFlouroscopyRegistration.util.itk_helpers.create_itk_image_region'''

import unittest
import itk
from StereoFlouroscopyRegistration.util.itk_helpers import create_itk_image_region

class TestCreateITKImageRegion(unittest.TestCase):
    '''Test class for StereoFlouroscopyRegistration.util.itk_helpers.create_itk_image_region'''

    def test_index_different_length_than_dimensions(self):
        '''Test that create_itk_image_region asserts when index does not have
        length the same size as the image dimensions'''
        dimension = 3
        index = [1]
        size = [1, 2, 3]
        with self.assertRaises(AssertionError):
            create_itk_image_region(dimension, index, size)

    def test_size_different_length_than_dimensions(self):
        '''Test that create_itk_image_region asserts when index does not have
        length the same size as the image dimensions'''
        dimension = 3
        index = [1, 2, 3]
        size = [1, 2, 3, 4]
        with self.assertRaises(AssertionError):
            create_itk_image_region(dimension, index, size)

    def test_create_valid_region_d3(self):
        '''Test that create_itk_image_region creates a valid itkImageRegion
        with dimensions equal to 3'''
        # Inputs
        dimension = 3
        index = [0, 1, 2]
        size = [100, 200, 300]

        # Create our own image region
        this_index = itk.Index[3]()
        this_index[0] = 0
        this_index[1] = 1
        this_index[2] = 2

        this_size = itk.Size[3]()
        this_size[0] = 100
        this_size[1] = 200
        this_size[2] = 300

        this_region = itk.ImageRegion[3]()
        this_region.SetSize(this_size)
        this_region.SetIndex(this_index)

        # Assert equal
        created_region = create_itk_image_region(dimension, index, size)
        self.assertEqual(this_region, created_region)
