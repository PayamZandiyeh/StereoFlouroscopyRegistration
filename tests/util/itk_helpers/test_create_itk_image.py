'''Test StereoFlouroscopyRegistration.util.itk_helpers.create_itk_image'''

import unittest
import itk
from StereoFlouroscopyRegistration.util.itk_helpers import create_itk_image

class TestCreateITKImage(unittest.TestCase):
    '''Test class for StereoFlouroscopyRegistration.util.itk_helpers.create_itk_image'''

    def test_create_3d_image_successful(self):
        '''Test that create_itk_image can create a 3D image.'''
        # Parameters
        dimension = 3
        pixel_string = 'unsigned char'
        pixel_type = itk.ctype(pixel_string)
        image_type = itk.Image[pixel_type, dimension]
        this_image = image_type.New()

        start = itk.Index[dimension]()
        start[0] = 0    # first index on X
        start[1] = 0    # first index on Y
        start[2] = 0    # first index on Z

        size = itk.Size[dimension]()
        size[0] = 200   # size along X
        size[1] = 200   # size along Y
        size[2] = 200   # size along Z

        image_region = itk.ImageRegion[dimension]()
        image_region.SetSize(size)
        image_region.SetIndex(start)

        this_image.SetRegions(image_region)
        this_image.Allocate()

        # Call method
        created_image = create_itk_image(dimension, pixel_string, image_region)

        # Need to compare the components
        self.assertEqual(this_image.GetImageDimension(), created_image.GetImageDimension())
        self.assertEqual(this_image.GetDirection(), created_image.GetDirection())
        self.assertEqual(this_image.GetLargestPossibleRegion(), \
          created_image.GetLargestPossibleRegion())
        self.assertEqual(this_image.GetOrigin(), created_image.GetOrigin())
        self.assertEqual(this_image.GetSpacing(), created_image.GetSpacing())
