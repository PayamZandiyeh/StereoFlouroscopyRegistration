'''Test StereoFlouroscopyRegistration.io.read_image.get_vtk_reader_from_file_name'''

import unittest
import shutil
import tempfile
import itk
import numpy as np
import os
from StereoFlouroscopyRegistration.util.itk_helpers import create_itk_image_region, create_itk_image
from StereoFlouroscopyRegistration.io.read_image import get_vtk_reader_from_file_name

class TestGetVTKReaderFromFileName(unittest.TestCase):
    '''Test class for StereoFlouroscopyRegistration.io.read_image.get_vtk_reader_from_file_name'''

    def setUp(self):
        '''Setup for TestGetVTKReaderFromFileName'''
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

    def tearDown(self):
        '''Tear down for TestGetVTKReaderFromFileName'''
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def test_files_exist(self):
        '''Test that setUp creates the images we expect'''
        for file_name in self.file_names:
            self.assertTrue(os.path.isfile(file_name))

    def test_non_existant_file_returns_none(self):
        '''Test that a non existant file returns none'''
        reader = get_vtk_reader_from_file_name(self.fake_file_name)
        self.assertEqual(reader, None)

    def test_nifti_reader(self):
        '''Test that the reader can be found for the nifti file'''
        reader = get_vtk_reader_from_file_name(self.nifti_file_name)
        self.assertNotEqual(reader, None)
        self.assertEqual(reader.GetClassName(), 'vtkNIFTIImageReader')

    def test_nifti_gz_reader(self):
        '''Test that the reader can be found for the nifti file gunzipped'''
        reader = get_vtk_reader_from_file_name(self.nifti_gz_file_name)
        self.assertNotEqual(reader, None)
        self.assertEqual(reader.GetClassName(), 'vtkNIFTIImageReader')

    def test_meta_reader(self):
        '''Test that the reader can be found for the meta file'''
        reader = get_vtk_reader_from_file_name(self.meta_file_name)
        self.assertNotEqual(reader, None)
        self.assertEqual(reader.GetClassName(), 'vtkMetaImageReader')

    def test_nrrd_reader(self):
        '''Test that the reader can be found for the nrrd file'''
        reader = get_vtk_reader_from_file_name(self.nrrd_file_name)
        self.assertNotEqual(reader, None)
        self.assertEqual(reader.GetClassName(), 'vtkNrrdReader')
