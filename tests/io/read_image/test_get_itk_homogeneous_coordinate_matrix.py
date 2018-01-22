'''Test StereoFlouroscopyRegistration.io.read_image.get_itk_homogeneous_coordinate_matrix'''

import unittest
import shutil
import tempfile
import itk
import numpy as np
import os
from StereoFlouroscopyRegistration.util.itk_helpers import create_itk_image_region, create_itk_image, set_itk_image_origin, set_itk_image_direction
from StereoFlouroscopyRegistration.io.read_image import get_itk_homogeneous_coordinate_matrix

class TestGetITKHomogeneousCoordinateMatrix(unittest.TestCase):
    '''Test class for StereoFlouroscopyRegistration.io.read_image.get_itk_homogeneous_coordinate_matrix'''

    def setUp(self):
        '''Set up for TestGetITKHomogeneousCoordinateMatrix'''
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

        # Create an image with a known orientation
        dimension = 3
        pixel_string = 'unsigned char'
        index = [0, 0, 0]
        size = [10, 10, 10]

        # Create image
        self.image_region = create_itk_image_region(dimension, index, size)
        self.image = create_itk_image(dimension, pixel_string, self.image_region)
        
        # Set origin
        self.origin = np.array([100, 200, 300])  # Origin in x,y,z
        set_itk_image_origin(self.image, self.origin)

        # This matrix represents an Euler angle rotation oriented XYZ with all angles 30
        alpha = 0.5000000
        beta = 0.8660254
        self.direction_matrix = np.array([
            [  0.7500000, -0.4330127,  0.5000000],
            [0.6495190,  0.6250000, -0.4330127],
            [-0.1250000,  0.6495190,  0.7500000 ]])
        set_itk_image_direction(self.image, self.direction_matrix)

        # Save image
        self.nifti_file_name = os.path.join(self.test_dir, 'nifti.nii')
        self.nifti_gz_file_name = os.path.join(self.test_dir, 'nifti.nii.gz')
        self.meta_file_name = os.path.join(self.test_dir, 'meta.mhd')
        self.nrrd_file_name = os.path.join(self.test_dir, 'nrrd.nrrd')

        self.file_names = [self.nifti_file_name, self.nifti_gz_file_name, self.meta_file_name, self.nrrd_file_name]
        for file_name in self.file_names:
            itk.imwrite(self.image, file_name)

        # Fake image for testing
        self.fake_file_name = os.path.join(self.test_dir, 'fake.file')

        # Create homogeneous matrix
        origin = np.array([self.origin])
        homo_coords = np.array([[0, 0, 0, 1]])
        self.homogeneous_matrx = np.concatenate((self.direction_matrix, origin.T), axis=1)
        self.homogeneous_matrx = np.concatenate((self.homogeneous_matrx, homo_coords), axis=0)

    def tearDown(self):
        '''Tear down for TestGetITKHomogeneousCoordinateMatrix'''
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def test_files_exist(self):
        '''Test that setUp creates the images we expect'''
        for file_name in self.file_names:
            self.assertTrue(os.path.isfile(file_name))

    def test_non_existant_file_returns_none(self):
        '''Test that a non existant file returns none'''
        orientation = get_itk_homogeneous_coordinate_matrix(self.fake_file_name)
        self.assertEqual(orientation, None)

    def test_nifti_orientation_test(self):
        '''Test that the orientation (and origin) can be set for the nifti file'''
        orientation = get_itk_homogeneous_coordinate_matrix(self.nifti_file_name)
        self.assertTrue(np.allclose(self.homogeneous_matrx, orientation))

    def test_nifti_gz_orientation_test(self):
        '''Test that the orientation (and origin) can be set for the nifti file gunzipped'''
        orientation = get_itk_homogeneous_coordinate_matrix(self.nifti_gz_file_name)
        self.assertTrue(np.allclose(self.homogeneous_matrx, orientation))

    def test_meta_orientation_test(self):
        '''Test that the orientation (and origin) can be set for the meta file'''
        orientation = get_itk_homogeneous_coordinate_matrix(self.meta_file_name)
        self.assertTrue(np.allclose(self.homogeneous_matrx, orientation))

    def test_nrrd_orientation_test(self):
        '''Test that the orientation (and origin) can be set for the nrrd file'''
        orientation = get_itk_homogeneous_coordinate_matrix(self.nrrd_file_name)
        self.assertTrue(np.allclose(self.homogeneous_matrx, orientation))
