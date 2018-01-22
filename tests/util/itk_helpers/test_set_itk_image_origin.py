'''Test StereoFlouroscopyRegistration.util.itk_helpers.set_itk_image_origin'''

import unittest
import itk
from StereoFlouroscopyRegistration.util.itk_helpers import *

class TestSetITKImageOrigin(unittest.TestCase):
    '''Test class for StereoFlouroscopyRegistration.util.itk_helpers.set_itk_image_origin'''

    def setUp(self):
        '''Set up for TestSetITKImageOrigin'''
        #
        self.dimension = 3
        self.index = [0, 0, 0]
        self.size = [100, 100, 100]
        self.pixel_string = 'unsigned char'

        # Create image
        self.image_region = create_itk_image_region(self.dimension, self.index, self.size)
        self.image = create_itk_image(self.dimension, self.pixel_string, self.image_region)

    def test_setup_correctly(self):
        '''Test that TestSetITKImageOrigin setup the test correctly.'''
        self.assertEqual(self.image.GetImageDimension(), 3)
        self.assertEqual(self.image.GetLargestPossibleRegion(), self.image_region)

    def test_assert_when_origin_different_size_than_dimension(self):
        '''Test that an origin with a different size than the dimensions
        of the image asserts failure in set_itk_image_origin.'''
        origin = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        with self.assertRaises(AssertionError):
            set_itk_image_origin(self.image, origin)

    def test_origin_changes(self):
        '''Test that set_itk_image_origin actually sets the origin'''
        for ii in range(self.image.GetImageDimension()):
            self.assertEqual(self.image.GetOrigin()[ii], 0)

        new_origin = [1, 2, 3]
        set_itk_image_origin(self.image, new_origin)

        for ii in range(self.image.GetImageDimension()):
            self.assertEqual(self.image.GetOrigin()[ii], new_origin[ii])
