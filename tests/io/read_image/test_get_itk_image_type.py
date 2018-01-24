'''Test StereoFlouroscopyRegistration.io.read_image.get_itk_image_type'''

import os
import unittest
import shutil
import tempfile
import itk
import numpy as np
from StereoFlouroscopyRegistration.util.itk_helpers import \
    create_itk_image_region, create_itk_image
from StereoFlouroscopyRegistration.io.read_image import get_itk_image_type

class TestGetITKImageType(unittest.TestCase):
    '''Test class for StereoFlouroscopyRegistration.io.read_image.get_itk_image_type'''

    def setUp(self):
      '''Set up for TestGetITKImageType'''
      # Create a temporary directory
      self.test_dir = tempfile.mkdtemp()

      # Create an image with a known orientation
      pixel_types_as_strings = ['short', 'unsigned short', 'unsigned char']
      dimensions = [2, 3]
      extensions = ['nii', 'nii.gz', 'mhd', 'nrrd']

      # Create a bunch of files
      self.image_type_map = {}
      self.file_names = []
      for pixel_type_as_string in pixel_types_as_strings:
          for dimension in dimensions:
              # Create image
              index = [0 for x in range(dimension)]
              size = [10 for x in range(dimension)]
              image_region = create_itk_image_region(dimension, index, size)
              image = create_itk_image(dimension, pixel_type_as_string, image_region)

              image_type = itk.Image[itk.ctype(pixel_type_as_string), dimension]

              for extension in extensions:
                  # Create file name
                  file_name = os.path.join(self.test_dir, 'image_{}_{}.{}'.format(pixel_type_as_string, dimension, extension))
                  self.file_names.append(file_name)
                  self.image_type_map[file_name] = image_type

                  # Write image out
                  itk.imwrite(image, file_name)

    def tearDown(self):
      '''Tear down for TestGetITKImageType'''
      # Remove the temporary directory after the test
      shutil.rmtree(self.test_dir)

    def test_files_exist(self):
      '''Test that setUp creates the images we expect'''
      for file_name in self.file_names:
          self.assertTrue(os.path.isfile(file_name))

    def test_corret_image_type(self):
      '''Test that the correct image type is returned'''
      for file_name in self.file_names:
          self.assertEqual(self.image_type_map[file_name], get_itk_image_type(file_name))
    
