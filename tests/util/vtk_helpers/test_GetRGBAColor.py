'''Test StereoFlouroscopyRegistration.util.vtk_helpers.GetRGBAColor'''

import unittest
from StereoFlouroscopyRegistration.util.vtk_helpers import GetRGBAColor

class TestGetRGBAColor(unittest.TestCase):
    '''Test class for StereoFlouroscopyRegistration.util.vtk_helpers.GetRGBAColor'''

    def test_bad_color_name(self):
        '''Test that a bad color name returns black'''
        expected_rgba_value = [0.0, 0.0, 0.0, 1.0]
        rgba = GetRGBAColor('bad_color_name')

        self.assertEqual(expected_rgba_value, rgba)

    def test_white_color(self):
        '''Test that a bad color name returns black'''
        expected_rgba_value = [1.0, 1.0, 1.0, 1.0]
        rgba = GetRGBAColor('white')

        self.assertEqual(expected_rgba_value, rgba)

    def test_black_color(self):
        '''Test that a bad color name returns black'''
        expected_rgba_value = [0.0, 0.0, 0.0, 1.0]
        rgba = GetRGBAColor('black')

        self.assertEqual(expected_rgba_value, rgba)
