'''Test StereoFlouroscopyRegistration.util.vtk_helpers.GetRGBColor'''

import unittest
import vtk
from StereoFlouroscopyRegistration.util.vtk_helpers import GetRGBColor

class TestGetRGBColor(unittest.TestCase):
    '''Test class for StereoFlouroscopyRegistration.util.vtk_helpers.GetRGBColor'''

    def test_bad_color_name(self):
        '''Test that a bad color name returns black'''
        expected_rgb_value = [0.0, 0.0, 0.0]
        rgb = GetRGBColor('bad_color_name')

        self.assertEqual(expected_rgb_value, rgb)

    def test_white_color(self):
        '''Test that a bad color name returns black'''
        expected_rgb_value = [1.0, 1.0, 1.0]
        rgb = GetRGBColor('white')

        self.assertEqual(expected_rgb_value, rgb)

    def test_black_color(self):
        '''Test that a bad color name returns black'''
        expected_rgb_value = [0.0, 0.0, 0.0]
        rgb = GetRGBColor('black')

        self.assertEqual(expected_rgb_value, rgb)
