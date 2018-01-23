'''Test StereoFlouroscopyRegistration.util.itk_helpers.set_itk_image_direction'''

import unittest
import itk
from StereoFlouroscopyRegistration.util.itk_helpers import *

class TestSetITKImageDirection(unittest.TestCase):
    '''Test class for StereoFlouroscopyRegistration.util.itk_helpers.set_itk_image_direction'''

    def setUp(self):
        '''Set up for TestSetITKImageDirection'''
        #
        self.dimension = 3
        self.index = [0, 0, 0]
        self.size = [100, 100, 100]
        self.pixel_string = 'unsigned char'

        # Create image
        self.image_region = create_itk_image_region(self.dimension, self.index, self.size)
        self.image = create_itk_image(self.dimension, self.pixel_string, self.image_region)

    def test_setup_correctly(self):
        '''Test that TestSetITKImageDirection setup the test correctly.'''
        self.assertEqual(self.image.GetImageDimension(), 3)
        self.assertEqual(self.image.GetLargestPossibleRegion(), self.image_region)

    def test_direction_changes(self):
        '''Test that set_itk_image_direction actually sets the direction matrix'''
        # Test the input is as expected
        dimension = self.image.GetImageDimension()
        vnl_matrix = self.image.GetDirection().GetVnlMatrix()
        for ii in range(dimension):
            for jj in range(dimension):
                if ii == jj:
                    self.assertEqual(vnl_matrix.get(ii, jj), 1)
                else:
                    self.assertEqual(vnl_matrix.get(ii, jj), 0)

        # This matrix comes from a 60 degree rotation around x
        alpha = 0.5000000
        beta = 0.8660254
        direction_matrix = np.array([[1, 0, 0], [0, alpha, -beta], [0, beta, alpha]])
        set_itk_image_direction(self.image, direction_matrix)

        # Test the change
        new_vnl_matrix = self.image.GetDirection().GetVnlMatrix()
        for ii in range(dimension):
            for jj in range(dimension):
                self.assertEqual(new_vnl_matrix.get(ii, jj), direction_matrix[ii][jj])
