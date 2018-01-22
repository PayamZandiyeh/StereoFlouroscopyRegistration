'''Test StereoFlouroscopyRegistration.util.vtk_helpers.create_vtkMatrix4x4'''

import unittest
import vtk
import numpy as np
from StereoFlouroscopyRegistration.util.vtk_helpers import create_vtkMatrix4x4

class TestCreatevtkMatrix4x4(unittest.TestCase):
    '''Test class for StereoFlouroscopyRegistration.util.vtk_helpers.create_vtkMatrix4x4'''

    def test_create_vtkMatrix4x4_asserts_on_input_of_size_one(self):
        '''Test that a matrix of size one asserts.'''
        orientation = np.matrix([1])

        with self.assertRaises(AssertionError):
            matrix = create_vtkMatrix4x4(orientation)

    def test_create_vtkMatrix4x4_asserts_on_input_of_size_4x3(self):
        '''Test that a matrix of size 4x3 asserts.'''
        orientation = np.matrix([[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])

        with self.assertRaises(AssertionError):
            matrix = create_vtkMatrix4x4(orientation)

    def test_create_vtkMatrix4x4_asserts_on_input_of_size_3x4(self):
        '''Test that a matrix of size 3x4 asserts.'''
        orientation = np.matrix([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])

        with self.assertRaises(AssertionError):
            matrix = create_vtkMatrix4x4(orientation)

    def test_create_vtkMatrix4x4_creates_valid_matrix(self):
        '''Test that a matrix of size 3x4 asserts.'''
        orientation = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]])
        matrix = create_vtkMatrix4x4(orientation)

        self.assertTrue(isinstance(matrix, vtk.vtkMatrix4x4))
        for ii in range(4):
            for jj in range(4):
                self.assertEqual(orientation[ii][jj], matrix.GetElement(ii, jj))
