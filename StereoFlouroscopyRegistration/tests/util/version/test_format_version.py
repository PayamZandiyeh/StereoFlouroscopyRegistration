'''Test StereoFlouroscopyRegistration.util.version.format_version'''

import unittest
from StereoFlouroscopyRegistration.util.version import format_version

class TestFormatVersion(unittest.TestCase):
    '''Test class for StereoFlouroscopyRegistration.util.version.format_version'''

    def test_basic_version(self):
        '''Formatting a basic version string is correct'''
        self.assertEqual(format_version('v1.0.1'), 'v1.0.1')

    def test_version_with_double_digits(self):
        '''Formatting a double-digit version string is correct'''
        self.assertEqual(format_version('v10.00.101'), 'v10.0.101')

    def test_exception_on_empty(self):
        '''Throw exception on empty version string'''
        with self.assertRaises(EnvironmentError):
            format_version('')

    def test_exception_on_single_digit(self):
        '''Throw exception on a single digit version string'''
        with self.assertRaises(EnvironmentError):
            format_version('v1')

    def test_exception_on_double_digit(self):
        '''Throw exception on a double digit version string'''
        with self.assertRaises(EnvironmentError):
            format_version('v1.1')

    def test_exception_on_quad_digit(self):
        '''Throw exception on a quadruple digit version string'''
        with self.assertRaises(EnvironmentError):
            format_version('v1.1.1.1')

    def test_case_insensitive(self):
        '''Version is insensitive to the case of V'''
        self.assertEqual(format_version('v1.0.1'), 'v1.0.1')
        self.assertEqual(format_version('V1.0.1'), 'v1.0.1')

if __name__ == '__main__':
    unittest.main()
